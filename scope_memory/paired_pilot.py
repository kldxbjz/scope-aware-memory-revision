import json
from pathlib import Path

def build():
    families=[("drink","tea","coffee","office","train"),("answer_length","brief","detailed","math","validation"),("travel","train","plane","overseas","test")]
    items=[]
    for attr,old,new,ctx,split in families:
        for kind in ("exception","update"):
            initial=f"My usual preference for {attr} is {old}."
            change=(f"For {ctx} only, use {new}; otherwise keep {old}." if kind=="exception" else f"From now on, my usual preference for {attr} is {new}, replacing {old}.")
            items.append({"family":attr,"split":split,"kind":kind,
                "dialogue":[{"role":"user","content":initial},{"role":"user","content":change}],
                "gold":{"attribute":attr,"general":old if kind=="exception" else new,
                        "scopes":{ctx:new} if kind=="exception" else {}}})
    return items

def inference_input(item):
    # Labels/family/kind/split/gold never enter model-visible input.
    return [{"role":t["role"],"content":t["content"]} for t in item["dialogue"]]

if __name__=="__main__":
    print(json.dumps(build(),indent=2))
