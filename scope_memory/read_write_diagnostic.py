"""Evaluation-only fictional controls. No learned model or NL extraction claim."""
import copy
import json
from .paired_pilot import build

def families():
    items=build()
    for ex in (x for x in items if x["kind"]=="exception"):
        update=next(x for x in items if x["family"]==ex["family"] and x["kind"]=="update")
        context,new=next(iter(ex["gold"]["scopes"].items()))
        yield ex,update,context,new

def read_input(memory, attribute, situation):
    # Controlled correct memory is intentionally supplied for read-only diagnosis.
    # Expected answers, variant kind, family split, and gold transitions are excluded.
    return {"memory":copy.deepcopy(memory),"request":f"What is my preference for {attribute}?",
            "situation":situation}

def reader(payload, mode="correct"):
    m=payload["memory"]
    if mode=="overapply" and m["scopes"]:
        return next(iter(m["scopes"].values()))
    if mode=="ignore_scope":
        return m["general"]
    return m["scopes"].get(payload["situation"],m["general"])

def metric(errors,total):
    return {"errors":errors,"denominator":total,"rate":errors/total if total else None}

def read_diagnostic(read_fn):
    errors=positive_errors=negative_errors=pairs=mutations=0
    for ex,_,context,new in families():
        memory=copy.deepcopy(ex["gold"]); before=copy.deepcopy(memory)
        outcomes=[]
        for situation,expected in ((context,new),("ordinary",memory["general"])):
            payload=read_input(memory,ex["family"],situation)
            original=copy.deepcopy(payload)
            wrong=read_fn(payload)!=expected
            mutations+=payload!=original
            outcomes.append(wrong)
        positive_errors+=outcomes[0]; negative_errors+=outcomes[1]
        errors+=sum(outcomes);pairs+=not any(outcomes)
        assert memory==before
    return {"applicability":metric(errors,6),"scoped_side":metric(positive_errors,3),
            "ordinary_side":metric(negative_errors,3),"both_sides_correct":{"count":pairs,"denominator":3},
            "read_input_mutations":mutations,"writes_performed":0}

def write_diagnostic(mode="correct"):
    # Writer controls consume oracle transitions, NOT text. Isolate write-state faults.
    overwrite=missed=qa_errors=0
    for ex,update,context,new in families():
        old=ex["gold"]["general"]
        for variant in (ex,update):
            memory={"attribute":ex["family"],"general":old,"scopes":{}}
            def probe(situation,expected):
                return reader(read_input(memory,ex["family"],situation))!=expected
            qa_errors+=probe("ordinary",old)  # before any write
            target=copy.deepcopy(variant["gold"])
            if mode=="persist_exception" and variant["kind"]=="exception":
                target={"attribute":ex["family"],"general":new,"scopes":{}}
            if mode=="drop_update" and variant["kind"]=="update":
                target=copy.deepcopy(memory)
            memory=target
            if variant["kind"]=="exception":
                overwrite+=memory["general"]!=old
            else:
                missed+=memory["general"]!=new
            qa_errors+=probe(context,new)
            expected_after=old if variant["kind"]=="exception" else new
            qa_errors+=probe("ordinary",expected_after)
    return {"false_overwrite":metric(overwrite,3),"missed_durable_update":metric(missed,3),
            "chronological_probe_errors":metric(qa_errors,18)}

def run():
    return {"warning":"fictional deterministic negative controls; not SFT or empirical model performance",
            "read_only":{m:read_diagnostic(lambda p:reader(p,m)) for m in ("correct","overapply","ignore_scope")},
            "write_only":{m:write_diagnostic(m) for m in ("correct","persist_exception","drop_update")}}
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
