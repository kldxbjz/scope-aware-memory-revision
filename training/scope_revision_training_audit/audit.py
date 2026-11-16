"""CPU-only leakage/cue audit. Never trains a model or alters input artifacts."""
import argparse, hashlib, json, re
from collections import Counter
from fractions import Fraction
from pathlib import Path

def read(path):
    rows=[json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError(f'duplicate IDs: {path}')
    return rows

def joined(path,key=None):
    rows=read(path)
    if key:
        keys={r['id']:r for r in read(key)}
        if set(keys)!=set(r['id'] for r in rows): raise ValueError('key/input ID mismatch')
        rows=[dict(keys[r['id']],**r) for r in rows]
    return rows

def norm(s): return ' '.join(re.findall(r'[a-z0-9]+',s.lower()))
def messages(r): return r.get('prefix',r.get('messages',r.get('input',r.get('prompt',[]))))
def txt(r,view='full'):
    m=messages(r)
    if isinstance(m,str):
        try: m=json.loads(m)
        except json.JSONDecodeError: return m if view=='full' else ''
    if isinstance(m,dict):
        if view=='full': return json.dumps(m,sort_keys=True)
        m=m.get('conversation',[])
    if view=='last_user_only':
        m=[x for x in m if x.get('role')=='user'][-1:]
    elif view=='assistant_only': m=[x for x in m if x.get('role')=='assistant']
    return '\n'.join(x.get('text',x.get('content','')) for x in m)
def label(r): return r.get('action',r.get('intended_action'))
def group(r,k): return r.get(k) or None

def overlaps(a,b):
    out={}
    for k in ('id','family','domain','domain_family','template_family','contrast_group'):
        # Domain/family names are provenance hints, not semantic independence proof.
        aa={norm(str(r[k])) for r in a if r.get(k)}
        bb={norm(str(r[k])) for r in b if r.get(k)}
        out[k]=sorted(aa&bb)
    for view in ('full','last_user_only','assistant_only'):
        aa={norm(txt(r,view)):r['id'] for r in a if norm(txt(r,view))}
        bb={norm(txt(r,view)):r['id'] for r in b if norm(txt(r,view))}
        out['exact_normalized_'+view]=[{'a':aa[t],'b':bb[t]} for t in sorted(aa.keys()&bb.keys())]
    return out

def cue_probe(rows,view):
    def feat(s):
        t=norm(s).split(); return set(zip(t,t[1:],t[2:]))
    fs={r['id']:feat(txt(r,view)) for r in rows}
    groups=('family','domain_family','template_family','contrast_group')
    total=Fraction(); n=0; excluded=0
    for r in rows:
        candidates=[q for q in rows if q['id']!=r['id'] and all(not group(r,k) or group(r,k)!=group(q,k) for k in groups)]
        if not candidates: excluded+=1; continue
        sims=[]
        for q in candidates:
            a,b=fs[r['id']],fs[q['id']]
            sims.append((Fraction(len(a&b),max(1,len(a|b))),label(q)))
        best=max(x for x,y in sims); labels={y for x,y in sims if x==best}
        total+=Fraction(label(r) in labels,len(labels)); n+=1
    return {'n_evaluable':n,'no_disjoint_neighbor':excluded,'expected_correct_uniform_label_ties':float(total),
            'accuracy':float(total/n) if n else None,'excluded_same_groups':groups,
            'interpretation':'Lexical trigram nearest-neighbor cue probe, not model performance or proof of no leakage.'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--records',required=True);p.add_argument('--key')
    p.add_argument('--reference',action='append',default=[],help='BLIND_JSONL::KEY_JSONL (repeat)')
    p.add_argument('--crud');p.add_argument('--scope');p.add_argument('--out')
    args=p.parse_args(); rows=joined(args.records,args.key)
    if any(label(r) is None for r in rows): raise ValueError('action/intended_action absent')
    result={'source_sha256':hashlib.sha256(Path(args.records).read_bytes()).hexdigest(),'n':len(rows),'labels':dict(Counter(label(r) for r in rows)),
      'cross_reference':{},'cue_probes':{v:cue_probe(rows,v) for v in ('last_user_only','assistant_only')},
      'limits':['Exact text and metadata overlap checks cannot establish semantic or template independence. Review domain aliases and paraphrases separately.',
                'Last-user-only cues may legitimately identify explicit instructions; same-final-turn contrasting labels are the stronger context-dependence test.',
                'No trained-model or heldout performance is measured.']}
    result['split_overlaps']={}
    splits=sorted({r.get('split','unspecified') for r in rows})
    for i,s in enumerate(splits):
        for t in splits[i+1:]: result['split_overlaps'][s+' vs '+t]=overlaps([r for r in rows if r.get('split','unspecified')==s],[r for r in rows if r.get('split','unspecified')==t])
    for ref in args.reference:
        parts=ref.split('::');result['cross_reference'][ref]=overlaps(rows,joined(*parts))
    groups={}
    for r in rows: groups.setdefault(norm(txt(r,'last_user_only')),[]).append(r)
    result['same_final_turn_contrasts']=[{'ids':[r['id'] for r in rr],'labels':sorted({label(r) for r in rr})} for text,rr in groups.items() if text and len({label(r) for r in rr})>1]
    if bool(args.crud)!=bool(args.scope): raise ValueError('supply both --crud and --scope')
    if args.crud:
        a={r['id']:r for r in read(args.crud)};b={r['id']:r for r in read(args.scope)}
        result['arm_input_identity']={'same_ids':a.keys()==b.keys(),'unequal_inputs':[i for i in a.keys()&b.keys() if messages(a[i])!=messages(b[i])],
          'note':'Exact visible inputs only; target semantics and training hyperparameters require separate checks.'}
    s=json.dumps(result,indent=2);print(s)
    if args.out:Path(args.out).write_text(s+'\n')
if __name__=='__main__':main()
