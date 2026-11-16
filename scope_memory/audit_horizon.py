import json,hashlib,sys,argparse
from pathlib import Path

REVISION="50941f00f90c03a5a60219d76393869b757b835a"
SOURCE="https://datasets-server.huggingface.co/rows?dataset=stellalisy%2FHorizonBench&config=mental_state_graphs&split=test&offset=0&length=3"

def decoded(row,key):
    value=row[key]
    return json.loads(value) if isinstance(value,str) else value

def visible_prefix(conversations, date, conversation_index=None, turn_index=None):
    """Date-only means end-of-date. Index tie-break is engineering, not proven chronology."""
    cutoff=(date, conversation_index if conversation_index is not None else float("inf"),
            turn_index if turn_index is not None else float("inf"))
    out=[]
    for ci,conv in sorted(enumerate(conversations),key=lambda x:(x[1]["date"],x[0])):
        for ti,turn in enumerate(conv["conversation"]["turns"]):
            if (conv["date"],ci,ti)>cutoff:
                continue
            out.append({"date":conv["date"],"role":turn["role"],"content":turn["content"]})
    return out

def audit(payload):
    users=[]; seen_users=set()
    for wrapper in payload["rows"]:
        if wrapper.get("truncated_cells"):
            raise ValueError("Refuse truncated source rows")
        row=wrapper["row"]
        uid=row["user_id"]
        if uid in seen_users: raise ValueError("duplicate user")
        seen_users.add(uid)
        prefs=decoded(row,"preference_record")
        convs=decoded(row,"conversations")
        changes={}; expressed={}
        for date, states in sorted(prefs.items()):
            for sid,state in states.items():
                for change in state.get("evolution_history",[]):
                    key=json.dumps([sid,change],sort_keys=True)
                    changes[key]=(sid,change)
        for c in convs:
            for i,t in enumerate(c["conversation"]["turns"]):
                if t["role"]=="user":
                    for sid in t.get("preference_expressed",{}):
                        expressed.setdefault(sid,[]).append((c["date"],i))
        entries=[]
        for sid,change in changes.values():
            dt=change["date"]
            candidates=sorted(x for x in expressed.get(sid,[]) if x[0]>=dt)
            entries.append({"structure_id":sid,"latent_date":dt,
                "changed_attributes":len(change.get("attribute_changes",{})),
                "first_later_annotated_turn":candidates[0] if candidates else None,
                "first_verified_observable_evidence":None,
                "label":"ambiguous_or_unverified"})
        users.append({"user_hash":hashlib.sha256(uid.encode()).hexdigest(),
            "split":"audit_only_exclude_from_training_and_final_test",
            "generator":row["generator"],"snapshot_dates":len(prefs),
            "conversations":len(convs),"unique_latent_change_records":len(entries),
            "changed_attribute_instances":sum(x["changed_attributes"] for x in entries),
            "later_annotated_turn_candidates":sum(x["first_later_annotated_turn"] is not None for x in entries),
            "definite_global_revision":0,"definite_scoped_exception":0,
            "ambiguous_or_unverified":len(entries),"changes":entries})
    return {"source_revision":REVISION,"endpoint":SOURCE,"selection":"row indices 0,1,2; not representative",
        "license":"CC-BY-4.0 (dataset card); code license separate",
        "counting_unit":"unique (user, structure_id, complete evolution_history record); repeated snapshots deduplicated",
        "semantic_review_status":"NOT completed: annotation anchors are candidates, not observable ground truth",
        "users":users}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output",required=True);a=p.parse_args()
    raw=Path(a.input).read_bytes();r=audit(json.loads(raw))
    r["response_sha256"]=hashlib.sha256(raw).hexdigest()
    Path(a.output).write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({"users":len(r["users"]),"latent_changes":sum(u["unique_latent_change_records"] for u in r["users"]),
        "changed_attributes":sum(u["changed_attribute_instances"] for u in r["users"]),
        "conversations":sum(u["conversations"] for u in r["users"]),
        "later_annotation_candidates":sum(u["later_annotated_turn_candidates"] for u in r["users"])}))
