"""Independent deterministic target replay, not natural-language label validation."""
import copy,json,sys
from pathlib import Path
from audit import read

def check(folder):
    p=Path(folder); labels={r['id']:r for r in read(p/'labels.jsonl')}; a={r['id']:r for r in read(p/'crud_sft.jsonl')};b={r['id']:r for r in read(p/'scope_sft.jsonl')}
    assert labels.keys()==a.keys()==b.keys()
    for i,r in labels.items():
        assert a[i]['prompt']==b[i]['prompt'],i
        sc=json.loads(b[i]['completion']);cu=json.loads(a[i]['completion']);before=r['pre_state'];state=copy.deepcopy(before)
        assert sc['action']==r['action'] and sc['decision']==cu['decision']==r['decision'],i
        c=sc['change']
        if r['action']=='set_default':
            assert c['kind']=='default';state['default']=c['value']
        elif r['action']=='set_exception':
            assert c['kind']=='exception';state['exceptions'][c['scope']]=c['value']
        else: assert r['action'] in ('no_op','defer') and c is None,i
        assert state==r['post_state'],i
        records={x['id']:x for x in json.loads(a[i]['prompt'])['memory']}
        for op in cu['operations']:
            if op['op']=='no_op': continue
            if op['op'] in ('add','update'):
                rec=op['record'];assert (rec['id'] in records)==(op['op']=='update'),i;records[rec['id']]=rec
            elif op['op']=='delete': del records[op['id']]
            else: raise AssertionError(op)
        assert records=={x['id']:x for x in r['canonical_post_records']},i
    return {'n':len(labels),'canonical_state_transitions':'PASS','crud_target_replay':'PASS','visible_prompt_identity':'PASS','limit':'Checks authored target algebra, not independent truth of conversational labels or a learned model.'}
if __name__=='__main__':print(json.dumps(check(sys.argv[1]),indent=2))
