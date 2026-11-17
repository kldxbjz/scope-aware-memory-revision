"""Spec format of the hand-written challenge episodes (training/challenge_v1/episodes/*.py).

Every module in episodes/ defines EPISODES, a list of dicts:

    {"name": "hotel-rooms",               # unique slug; the family becomes challenge-<stressor>-<name>
     "stressor": "dense",                 # one of STRESSORS
     "attributes": [{"attribute": "hotel room placement",
                     "options": ["a room on a high floor", ...],            # 4-6 natural phrases
                     "value_aliases": {"a room on a high floor": ["somewhere up high"]},
                     "scopes": {"conf": ("conference trips", ["work conferences"])}}],
     "initial": {"hotel room placement": ("a room on a high floor", {"conf": ("a room near the lifts", P)})},
     "events": [{"date": "2028-01-10", "category": "scoped_exception", "evidence": 3,
                 "change": ("add", "hotel room placement", "road", "a room overlooking the courtyard", P),
                 "dialogue": ["user", "assistant", "user"],                # alternating, the user first
                 "probes": [("target", "road"), ("neighbor", "conf"), ("default", None)],
                 "note": "why this is the gold change"}]}

change is None for stable_preference and clarify, or one of
    ("general", attribute, value)
    ("add", attribute, scope_key, value, validity)
    ("revise", attribute, scope_key, value, validity)
    ("retire", attribute, scope_key)
A probe is (probe_type, scope_key or None) on the changed attribute (or the only one) at the event date, or a dict
{"type": ..., "key": ..., "attribute": ..., "date": ...} to name another attribute or a later date. Values and
validities use the catalog names; build.py computes the states, the probe answers, the options and the ids.
"""
P = {"kind": "persistent"}
O = {"kind": "open"}
STRESSORS = ("dense", "shared", "confusable", "chain", "temporal", "distractor")


def W(start, end):
    """A window validity, both ends inclusive."""
    return {"kind": "window", "from": start, "to": end}
