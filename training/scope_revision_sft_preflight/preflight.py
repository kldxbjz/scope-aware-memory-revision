"""Offline CPU raw prompt/completion collator preflight. No model load/train."""
import argparse,inspect,json,os
from pathlib import Path

def read(p):
 rows=[json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]
 assert len({r['id'] for r in rows})==len(rows),'duplicate IDs'
 return {r['id']:r for r in rows}
def parity(a,b):
 assert a.keys()==b.keys(),'arm IDs differ'
 assert all(a[i]['prompt']==b[i]['prompt'] and a[i]['split']==b[i]['split'] for i in a),'arm prompts/splits differ'
def guard(ids,maximum):
 if len(ids)>maximum:raise ValueError(f'overlength {len(ids)} > {maximum}; truncation forbidden')
def encode(row,tok,maximum):
 # Explicit plain-text protocol; no hidden role template. Boundary is checked in JOINT tokenization.
 prompt=row['prompt']+'\n'; target=row['completion']; full=prompt+target
 enc=tok(full,add_special_tokens=False,return_offsets_mapping=True)
 ids=list(enc['input_ids']); offsets=enc['offset_mapping']; boundary=len(prompt)
 if any(s<boundary<e for s,e in offsets):raise ValueError('token straddles prompt/completion boundary')
 mask=[int(s>=boundary and e>s) for s,e in offsets]
 assert any(mask),'empty target'; assert ids and offsets[-1][1]==len(full),'target not fully covered'
 ids.append(tok.eos_token_id); mask.append(1);guard(ids,maximum)
 return {'input_ids':ids,'completion_mask':mask,'labels':[i if m else -100 for i,m in zip(ids,mask)]}
def verify(batch,features,eos):
 for n,f in enumerate(features):
  ids=batch['input_ids'][n].tolist(); labels=batch['labels'][n].tolist();att=batch['attention_mask'][n].tolist();length=len(f['input_ids'])
  assert ids[:length]==f['input_ids'] and labels[:length]==f['labels'],'token/mask mismatch'
  assert all(x==-100 for x in labels[length:]) and att==[1]*length+[0]*(len(ids)-length),'padding has loss/attention'
  assert ids[length-1]==labels[length-1]==eos,'EOS not supervised'
  assert any(x!=-100 for x in labels[1:length]),'no shifted target'
def main():
 p=argparse.ArgumentParser();p.add_argument('--corpus',required=True);p.add_argument('--tokenizer');p.add_argument('--max-length',type=int,default=2048);p.add_argument('--source-only',action='store_true');args=p.parse_args()
 root=Path(args.corpus);a=read(root/'crud_sft.jsonl');b=read(root/'scope_sft.jsonl');parity(a,b)
 if args.source_only:
  print(json.dumps({'source_pair_parity':'PASS','n_each':len(a),'tokenizer_and_collator':'NOT_RUN'}));return
 if not args.tokenizer or not Path(args.tokenizer).is_dir():raise ValueError('explicit existing local tokenizer directory required')
 for k in ('HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE'):os.environ[k]='1'
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch,transformers,trl
 from transformers import AutoTokenizer
 from trl.trainer.sft_trainer import DataCollatorForLanguageModeling
 tok=AutoTokenizer.from_pretrained(args.tokenizer,local_files_only=True,trust_remote_code=False,use_fast=True)
 assert tok.is_fast and tok.eos_token_id is not None,'fast tokenizer + EOS required'
 pad=tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
 sig=inspect.signature(DataCollatorForLanguageModeling);kw={'pad_token_id':pad,'padding_free':False}
 legacy='completion_only_loss' in sig.parameters
 if legacy:kw['completion_only_loss']=True
 coll=DataCollatorForLanguageModeling(**kw)
 arms=[[encode(r,tok,args.max_length) for r in x.values()] for x in (a,b)]
 def run(fs):
  payload=[{k:v for k,v in f.items() if k in (('input_ids','completion_mask') if legacy else ('input_ids','labels'))} for f in fs]
  batch=coll(payload);assert batch['input_ids'].device.type=='cpu';verify(batch,fs,tok.eos_token_id)
 for fs in arms:
  for f in fs:run([f])
 longest=[max(fs,key=lambda x:len(x['input_ids'])) for fs in arms];shortest=min(arms[0]+arms[1],key=lambda x:len(x['input_ids']));run(longest+[shortest])
 try:guard(longest[0]['input_ids'],len(longest[0]['input_ids'])-1)
 except ValueError:pass
 else:raise AssertionError('too-short limit accepted')
 print(json.dumps({'status':'PASS_COLLATOR_ONLY','versions':{'torch':torch.__version__,'transformers':transformers.__version__,'trl':trl.__version__},'n_each':len(a),'lengths':[[min(map(lambda f:len(f['input_ids']),fs)),max(map(lambda f:len(f['input_ids']),fs))] for fs in arms],'too_short_rejected':True,'actual_trainer_preprocessing_and_model_loss':'NOT_RUN','protocol':'plain JSON prompt + newline + JSON completion + explicit EOS; no packing/chat template'},indent=2))
if __name__=='__main__':main()
