"""Only run after internal annotations are locked. No model calls."""
import json
from pathlib import Path
def score(gold, records):
 a=records["internal_a"];b=records["internal_b"]
 assert a["locked"] and b["locked"]
 left={a["alias_to_id"][k]:v for k,v in a["labels"].items()}
 right=b["labels"]
 assert set(left)==set(right)==set(gold)
 ids=sorted(gold)
 disagreements=[i for i in ids if left[i]!=right[i]]
 return {"count":len(ids),"agreement":sum(left[i]==right[i] for i in ids),
  "disagreements":disagreements,
  "internal_a_author_key_correct":sum(left[i]==gold[i]["label"] for i in ids),
  "internal_b_author_key_correct":sum(right[i]==gold[i]["label"] for i in ids),
  "per_class":{c:{"count":sum(gold[i]["label"]==c for i in ids),
   "a_correct":sum(gold[i]["label"]==c and left[i]==c for i in ids),
   "b_correct":sum(gold[i]["label"]==c and right[i]==c for i in ids)}
   for c in ("lasting_update","scoped_exception","insufficient")},
  "warning":"Internal same-model synthetic sanity only; not human agreement or data readiness"}
if __name__=="__main__":
 p=Path(__file__).parent
 print(json.dumps(score(json.loads((p/"blind_gold.json").read_text()),
  json.loads((p/"blind_locked_labels.json").read_text())),indent=2))
