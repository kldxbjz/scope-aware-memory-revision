import json, hashlib
from collections import Counter
from pathlib import Path
from build import text_state
P=Path(__file__).parent
def read(n):return [json.loads(x) for x in (P/(n+'.jsonl')).read_text().splitlines()]
x,y,c,s=map(read,['inputs','labels','crud_sft','scope_sft'])
assert len(x)==len(y)==len(c)==len(s)==160
assert len({r['id'] for r in x})==160
assert Counter(r['action'] for r in y)==dict.fromkeys(['set_default','set_exception','no_op','defer'],40)
for attr in ['domain_family','template_family','contrast_group']:
    a={r[attr] for r in x if r['split']=='train'}; b={r[attr] for r in x if r['split']=='dev'}
    assert not a&b,(attr,a&b)
for i in range(0,160,4):
    g=x[i:i+4]
    assert len({json.dumps(r['input']['conversation'][-1]) for r in g})==1
    assert len({json.dumps(r['input']['conversation'][1]) for r in g})==1
    assert len({json.dumps(r['input']['memory']) for r in g})==1
for a,b,cr,sc in zip(x,y,c,s):
    assert a['id']==b['id']==cr['id']==sc['id']
    assert cr['prompt']==sc['prompt']==json.dumps(a['input'],ensure_ascii=False,sort_keys=True)
    label=a['domain_family'].replace('_',' ')
    assert text_state(b['pre_state'],label)==a['input']['memory']
    assert text_state(b['post_state'],label)==b['canonical_post_records']
    post=json.loads(json.dumps(b['pre_state']))
    if b['action']=='set_default':post['default']=b['change']['value']
    elif b['action']=='set_exception':post['exceptions'][b['change']['scope']]=b['change']['value']
    assert post==b['post_state']
    records={r['id']:r for r in a['input']['memory']}
    for op in json.loads(cr['completion'])['operations']:
        if op['op']!='no_op': records[op['record']['id']]=op['record']
    assert sorted(records.values(),key=lambda r:r['id'])==sorted(b['canonical_post_records'],key=lambda r:r['id'])
    assert json.loads(cr['completion'])['decision']==b['decision']
    assert json.loads(sc['completion'])['action']==b['action']
assert sum(r['old_exception_replacement'] for r in y)==20
m=json.loads((P/'manifest.json').read_text())
for name,h in m['sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h
print('PASS: 160 records; 128 train/32 dev; 40 per action; 20 replacements; paired inputs, transitions, CRUD reconstruction, contrasts, split isolation, hashes')
