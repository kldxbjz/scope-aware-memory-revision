#!/usr/bin/env python3
"""Compile hand-authored split banks into protocol-v1 chronological episodes."""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import random
import re
import sys

# The snapshot must remain unchanged outside this directory.
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPLITS = ("train", "dev", "test")
SIZE = {"train": 600, "dev": 120, "test": 200}
PAIRS = {"train": 90, "dev": 60, "test": 80}
KINDS = ("persistent", "window", "open")
QA_GROUP = {"scoped_exception": "scoped_exception",
            "general_update": "general_update",
            "stable_preference": "stable_preference",
            "clarify": "stable_preference",
            "exception_revision": "exception_revision",
            "exception_retirement": "exception_revision"}
RATIONALE = {
    "add": "The user chooses a continuing setting for the named situation.",
    "revise": "The user changes the value attached to the existing situation, with its earlier validity unchanged.",
    "general": "The user changes their ordinarily selected value, not the separate situation rules.",
    "clarify": "The indicated choice is tentative and the user has not settled which situation it is for.",
    "resolve": "The user resolves the earlier uncertainty by choosing the situation with an existing rule.",
    "retire": "The separate instruction for the named situation is withdrawn; subsequent ordinary settings are inherited.",
    "stable": "This exchange does not communicate a change to the user's ongoing preferences.",
    "trial": "The choice is approved for the current instance only.",
}
# Branch-independent conversation chatter: supplied separately by each split bank when available.
QUESTIONS = {
    "train": "For {occ} on {day}, what is the selected {attribute}?",
    "dev": "It is {day} and the situation is {occ}. Which {attribute} would fit the preference?",
    "test": "Pick a value for {attribute}, dated {day}, with the setting described as {occ}.",
}
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def plain_day(d):
    return f"{MONTHS[d.month - 1]} {d.day}"


def record_id(prefix, episode, n):
    # Unique, neither event order nor category encoded in the opaque suffix.
    return prefix + hashlib.sha256(f"{prefix}/{episode}/{n}".encode()).hexdigest()[:20]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(payload)


def write_json(path, data):
    write(path, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def event_dialogue(row, args, branch=None):
    src = row["messages"] if branch is None else row["branches"][branch]
    rows = []
    for i, m in enumerate(src):
        role = m["role"] if isinstance(m, dict) else ("user" if i % 2 == 0 else "assistant")
        text = (m["content"] if isinstance(m,dict) else m).format_map(args)
        rows.append({"role": role, "content": text[:1].upper() + text[1:]})
    return rows


def episode(split, number, scenario, bank, rng, kind, contrast_group, branch,
            second_scenario=None):
    """Sample a legal trajectory, not a fixed sequence of category slots.

    Initial rules represent earlier conversations. At each turn only actions
    legal in the current state are eligible; random category choice happens
    before random attribute/situation choice. A pending question can resolve
    later, remain open, or be separated from its resolution by other business.
    Rendering and probe random streams cannot perturb the state-machine draw.
    """
    from surface import catalog_aliases, prepare_args, render

    eid = f"{split[:2]}-{number:04d}"
    scenes = [scenario] + ([second_scenario] if second_scenario else [])
    scene_of = {s["attribute"]: s for s in scenes}
    catalogs, state = [], {}
    base = date(2027, rng.randrange(1, 13), rng.randrange(2, 11))
    render_seed, probe_seed = rng.getrandbits(64), rng.getrandbits(64)
    probe_rng = random.Random(probe_seed)
    event_count = rng.randrange(4, 9)
    event_days = [base]
    for _ in range(event_count - 1):
        event_days.append(event_days[-1] + timedelta(days=rng.choice((1, 1, 2))))
    for scene in scenes:
        attribute = scene["attribute"]
        aliases = catalog_aliases(scene, split)
        catalogs.append({
            "attribute": attribute, "options": list(scene["options"]),
            "value_aliases": aliases["value_aliases"],
            "scopes": {key: {"scope": scope, "aliases": aliases["scope_aliases"][j]}
                       for j, (key, scope) in enumerate(zip(("focus", "adjacent"), scene["scopes"]))},
        })
        values = rng.sample(scene["options"], len(scene["options"]))
        current = {"general": values[0], "exceptions": {}}
        # Realistic empty, one-situation and two-situation seed memories.
        # Initial windows are avoided so every window in this release has an
        # observable creation event and its own immediate boundary probes.
        keys = rng.sample(["focus", "adjacent"], rng.randrange(3))
        for j, key in enumerate(keys):
            current["exceptions"][key] = {
                "value": values[j + 1],
                "validity": {"kind": rng.choice(("persistent", "open"))},
            }
        state[attribute] = current
    initial = deepcopy(state)
    catalog_of = {c["attribute"]: c for c in catalogs}
    events, details, probes = [], [], []
    pending, changed_attributes = {}, set()
    window_writes = 0
    stable_keys = sorted(k for k in bank if k.startswith("stable_"))
    # Each paired episode has one late focal contrast. Its ordinal varies
    # from four to eight, and an existing rule may be revised rather than added.
    contrast_at = event_count - 1 if contrast_group is not None else None

    def covering(rule, day):
        v = rule["validity"]
        return v["kind"] != "window" or v["from"] <= day.isoformat() <= v["to"]

    for i, day in enumerate(event_days):
        remaining = event_count - i - (1 if contrast_at is not None else 0)
        unmet = set(scene_of) - changed_attributes
        # Both attributes have an actual write, not a decorative second catalog.
        required = unmet if remaining <= len(unmet) else set()
        candidates = {action: [] for action in ("general", "add", "revise", "retire", "stable", "clarify")}
        for attribute, current in state.items():
            if required and attribute not in required:
                continue
            candidates["general"].append((attribute, None, "general"))
            if not required:
                candidates["stable"].append((attribute, None, "stable"))
            for key in ("focus", "adjacent"):
                rule = current["exceptions"].get(key)
                waiting = pending.get(attribute)
                reserved = waiting is not None and waiting["key"] == key
                if not rule and not reserved:
                    candidates["add"].append((attribute, key, "add"))
                if rule and not reserved:
                    candidates["retire"].append((attribute, key, "retire"))
                    if covering(rule, day) and (rule["validity"]["kind"] != "window" or window_writes < 2):
                        candidates["revise"].append((attribute, key, "revise"))
                if not required and waiting is None and (not rule or covering(rule, day)):
                    candidates["clarify"].append((attribute, key, "clarify"))
            if attribute in pending:
                waiting = pending[attribute]
                rule = current["exceptions"].get(waiting["key"])
                if not rule:
                    candidates["add"].append((attribute, waiting["key"], "resolve"))
                elif covering(rule, day) and (rule["validity"]["kind"] != "window" or window_writes < 2):
                    candidates["revise"].append((attribute, waiting["key"], "resolve"))
        if i == contrast_at:
            attribute = rng.choice(list(scene_of))
            available = [k for k in ("focus", "adjacent")
                         if attribute not in pending or pending[attribute]["key"] != k]
            scope_key = rng.choice(available)
            action = "contrast"
        else:
            resolutions = [entry for entries in candidates.values() for entry in entries
                           if entry[2] == "resolve"]
            # An unanswered question is often revisited, but the next turn can
            # still concern something else. Questions near the cutoff may stay
            # genuinely unresolved; no fixed resolve slot is appended.
            if resolutions and rng.random() < .50:
                attribute, scope_key, action = rng.choice(resolutions)
            else:
                eligible = [key for key, entries in candidates.items() if entries]
                category_action = rng.choice(eligible)
                attribute, scope_key, action = rng.choice(candidates[category_action])
        scene = scene_of[attribute]
        catalog = catalog_of[attribute]
        current = state[attribute]
        options = scene["options"]
        if scope_key is None:
            scope_key = rng.choice(("focus", "adjacent"))
        neighbor_key = "adjacent" if scope_key == "focus" else "focus"
        scope = catalog["scopes"][scope_key]["scope"]
        neighbor = catalog["scopes"][neighbor_key]["scope"]
        old_rule = current["exceptions"].get(scope_key)
        old = old_rule["value"] if old_rule else current["general"]
        choices = [x for x in options if x not in {old, current["general"]}]
        new = rng.choice(choices)
        validity = deepcopy(old_rule["validity"]) if old_rule else None
        selected_kind = validity["kind"] if validity else kind
        if action in {"add", "resolve"} and old_rule is None:
            selected_kind = kind if window_writes < 2 else rng.choice(("persistent", "open"))
            if selected_kind == "window":
                start = day + timedelta(days=rng.choice((0, 0, 1)))
                end = start + timedelta(days=rng.randrange(11, 24))
                validity = {"kind": "window", "from": start.isoformat(), "to": end.isoformat()}
            else:
                validity = {"kind": selected_kind}
        if action == "general":
            category, key = "general_update", "general"
            # General changes are immediate and continuing under the contract;
            # do not inherit a nearby situation's open/window duration in text.
            selected_kind = "persistent"
            avoid = {current["general"]}
            if attribute in pending:
                avoid.add(pending[attribute]["new"])
            new = rng.choice([x for x in options if x not in avoid])
        elif action == "add":
            category, key = "scoped_exception", "add_" + selected_kind
        elif action == "revise":
            category, key = "exception_revision", "revise"
        elif action == "stable":
            category, key = "stable_preference", rng.choice(stable_keys)
            if "reaffirm" in key:
                new = current["general"]
        elif action == "clarify":
            category, key = "clarify", "clarify"
            pending[attribute] = {"key": scope_key, "new": new}
        elif action == "resolve":
            category = "exception_revision" if old_rule else "scoped_exception"
            key, new = "resolve", pending.pop(attribute)["new"]
        elif action == "retire":
            category, key, new = "exception_retirement", "retire", current["general"]
        elif action == "contrast":
            category = (("exception_revision" if old_rule else "scoped_exception")
                        if branch == "persistent" else "stable_preference")
            key, selected_kind, validity = "contrast", "persistent", {"kind": "persistent"}
        else:
            raise AssertionError(action)
        # Non-window events still supply all legacy placeholders, although the
        # corresponding surface render never invents a calendar interval.
        window_start = date.fromisoformat(validity["from"]) if validity and selected_kind == "window" else day
        window_end = date.fromisoformat(validity["to"]) if validity and selected_kind == "window" else day + timedelta(days=14)
        start, end = plain_day(window_start), plain_day(window_end)
        date_phrase = rng.choice(bank["timing"][selected_kind]).format(start=start, end=end)
        row = rng.choice(bank[key])
        args = dict(attribute=attribute, scope=scope, neighbor=neighbor,
                    general=current["general"], old=old, new=new,
                    start=start, end=end, timing=date_phrase,
                    opener=scene["opener"], distraction=scene["distraction"],
                    alt=rng.choice([v for v in options if v != new]), date=plain_day(day),
                    adjacent=current["exceptions"].get(neighbor_key, {}).get("value", current["general"]),
                    kind=selected_kind, domain=scene["domain"],
                    has_focus=old_rule is not None,
                    has_neighbor=neighbor_key in current["exceptions"], stable_key=key)
        args = prepare_args(scene, args, split)
        surface_rng = random.Random(f"scope-surface/{render_seed}/{i}")
        msg, evidence = render(row, args, surface_rng, split, action,
                               branch if action == "contrast" else None)
        exception_changed = None
        if action == "general":
            current["general"] = new
        elif action in {"add", "revise", "resolve"} or (action == "contrast" and branch == "persistent"):
            exception_changed = deepcopy(validity)
            current["exceptions"][scope_key] = {"value": new, "validity": exception_changed}
            if validity["kind"] == "window":
                window_writes += 1
        elif action == "retire":
            del current["exceptions"][scope_key]
        if category not in {"clarify", "stable_preference"}:
            changed_attributes.add(attribute)
        report_action = ("revise" if old_rule else "add") if action == "contrast" and branch == "persistent" else (
                        "trial" if action == "contrast" else action)
        rationale = RATIONALE[report_action]
        if action == "resolve" and old_rule is None:
            rationale = "The user settles the earlier choice of situation and supplies a continuing instruction for it."
        if action == "contrast" and branch == "persistent" and old_rule:
            rationale = "The user chooses a continuing replacement for the existing situation rule."
        ev_id = record_id("e", eid, i)
        events.append({"event_id": ev_id, "date": day.isoformat(), "dialogue": msg,
                       "gold": {"category": category,
                                "decision": "clarify" if category == "clarify" else "resolved",
                                "state_after": deepcopy(state),
                                "evidence_message": evidence, "rationale": rationale}})
        details.append((action, attribute, scope_key, neighbor_key, exception_changed))
    assert changed_attributes == set(scene_of)
    # Every window write and focal contrast is evaluated. Additional checkpoints
    # are sampled without category-specific slots, and cover both attributes.
    checkpoints = {i for i, detail in enumerate(details)
                   if detail[-1] and detail[-1]["kind"] == "window"}
    if contrast_at is not None:
        checkpoints.add(contrast_at)
    for attribute in scene_of:
        if not any(details[i][1] == attribute for i in checkpoints):
            checkpoints.add(probe_rng.choice([i for i, d in enumerate(details) if d[1] == attribute]))
    checkpoint_count = max(len(checkpoints), probe_rng.randrange(2, 5))
    assert checkpoint_count <= 4
    remaining = [i for i in range(event_count) if i not in checkpoints]
    checkpoints.update(probe_rng.sample(remaining, checkpoint_count - len(checkpoints)))
    for i in sorted(checkpoints):
        ev = events[i]
        day = date.fromisoformat(ev["date"])
        action, attribute, scope_key, neighbor_key, exception_changed = details[i]
        current = ev["gold"]["state_after"][attribute]
        catalog = catalog_of[attribute]
        positions = [("target", scope_key, day), ("default", None, day), ("neighbor", neighbor_key, day)]
        if action == "general":
            positions = [("target", None, day), ("neighbor", scope_key, day), ("neighbor", neighbor_key, day)]
        if exception_changed and exception_changed["kind"] == "window":
            ws, we = date.fromisoformat(exception_changed["from"]), date.fromisoformat(exception_changed["to"])
            positions[0] = ("target", scope_key, max(day, ws))
            positions += [("target", scope_key, we), ("boundary", scope_key, we + timedelta(days=1))]
            if day < ws:
                positions += [("boundary", scope_key, ws - timedelta(days=1))]
        for typ, sk, pd in positions:
            occ = catalog["scopes"][sk]["scope"] if sk else "an ordinary occasion"
            active = current["exceptions"].get(sk)
            out = active["value"] if active and covering(active, pd) else current["general"]
            options = catalog["options"]
            probes.append({"probe_id": record_id("p", eid, len(probes)), "after_event": ev["event_id"],
                           "attribute": attribute,
                           "question": QUESTIONS[split].format(attribute=attribute, occ=occ, day=plain_day(pd)),
                           "date": pd.isoformat(), "situation_scope_keys": [sk] if sk else [],
                           "options": probe_rng.sample(options, len(options)), "gold": out,
                           "category": QA_GROUP[ev["gold"]["category"]], "probe_type": typ})
    return {"episode_id": eid, "split": split, "family": scenario["family"],
            "contrast_group": contrast_group, "attributes": catalogs,
            "initial_state": initial, "events": events, "probes": probes}


def make_split(split, rng):
    root = HERE / "banks" / split
    scenarios = read_json(root / "scenarios.json")
    bank = read_json(root / "phrasing.json")
    rotation = list(scenarios)
    rng.shuffle(rotation)
    # Stratify only the requested attribute-count proportion. Event labels,
    # number and order are sampled by the state machine above, never assigned
    # to fixed positions or adjusted to change a classifier's answers.
    pair_multis = set(rng.sample(range(PAIRS[split]), round(PAIRS[split] * .30)))
    singles = SIZE[split] - 2 * PAIRS[split]
    single_multis = set(rng.sample(range(singles), round(singles * .30)))
    specs = []
    for unit in range(SIZE[split] - PAIRS[split]):
        sc = rotation[unit % len(rotation)]
        kind = KINDS[(unit // len(rotation) + unit) % len(KINDS)]
        seed = rng.getrandbits(64)
        group = f"{split[:2]}-pair-{unit+1:04d}" if unit < PAIRS[split] else None
        multi = (unit in pair_multis) if group else (unit - PAIRS[split] in single_multis)
        peers = [s for s in scenarios if s["domain"] == sc["domain"] and s["attribute"] != sc["attribute"]]
        second = rng.choice(peers) if multi else None
        if group is not None:
            specs.extend(((sc, kind, seed, group, "persistent", second),
                          (sc, kind, seed, group, "one_off", second)))
        else:
            specs.append((sc, kind, seed, group, rng.choice(["persistent", "one_off"]), second))
    rng.shuffle(specs)
    return [episode(split, num, sc, bank, random.Random(sd), kind, group, branch, second)
            for num, (sc, kind, sd, group, branch, second) in enumerate(specs, 1)]


def markdown_samples(by_split, seed):
    blocks = ["# Thirty sampled episodes", "",
              "Ten complete episodes per split, independently sampled with a seeded PRNG.",
              "Contains evaluation gold: keep out of inference prompts and SFT inputs.", ""]
    rng = random.Random(f"scope-revision-samples/{seed}")
    for s, episodes in by_split.items():
        blocks += [f"## {s.title()}", ""]
        for ep in rng.sample(episodes,10):
            blocks += [f"### {ep['episode_id']} · {ep['family']}", "",
                       f"Contrast group: `{ep['contrast_group']}`", "",
                       "Initial state: `" + json.dumps(ep["initial_state"],ensure_ascii=False) + "`", ""]
            for e in ep["events"]:
                g = e["gold"]
                blocks += [f"**{e['date']} · {e['event_id']}**", ""]
                blocks += [f"- {d['role'].title()}: {d['content']}" for d in e["dialogue"]]
                blocks += [f"- Gold: {g['category']} / {g['decision']}; evidence message {g['evidence_message']}. {g['rationale']}",
                           "- After: `" + json.dumps(g["state_after"],ensure_ascii=False) + "`"]
                for q in ep["probes"]:
                    if q["after_event"] == e["event_id"]:
                        blocks += [f"- {q['probe_type']} QA: {q['question']} "
                                   f"Options: {' / '.join(q['options'])}. Gold: **{q['gold']}**."]
                blocks += [""]
    return "\n".join(blocks)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_overlap(by_split):
    """Check all four old releases using portable hashes, without copying old text."""
    def normalize(text):
        return " ".join(re.findall(r"[a-z0-9]+",text.casefold()))
    old = read_json(HERE/"banks"/"legacy_signatures.json")
    signature_counts = {}
    message_hashes, dialogue_hashes, labels = set(), set(), set()
    for rows in by_split.values():
        for ep in rows:
            labels.add(normalize(ep["family"]))
            labels.update(normalize(c["attribute"]) for c in ep["attributes"])
            for ev in ep["events"]:
                turns = [normalize(m["content"]) for m in ev["dialogue"]]
                msg_hash = (hashlib.sha256(x.encode()).hexdigest()
                            for x in turns if len(x.split()) >= 5)
                message_hashes.update(msg_hash)
                dialogue_hashes.add(hashlib.sha256("\n".join(turns).encode()).hexdigest())
    for source,sigs in old.items():
        overlap = {"old_examples":sigs["count"],
                   "same_dialogue":len(dialogue_hashes.intersection(sigs["normalized_dialogue_sha256"])),
                   "same_message_5plus_words":len(message_hashes.intersection(sigs["normalized_message_sha256"])),
                   "exact_known_domain_name_overlap":sorted(labels.intersection(
                       normalize(x) for x in sigs["known_domain_labels"]))}
        if overlap["same_dialogue"] or overlap["same_message_5plus_words"] or overlap["exact_known_domain_name_overlap"]:
            known = [m for rows in by_split.values() for ep in rows for e in ep["events"]
                     for m in e["dialogue"] if hashlib.sha256(normalize(m["content"]).encode()).hexdigest()
                     in sigs["normalized_message_sha256"]]
            raise ValueError(f"prior overlap {source} {overlap}; sample={known[:3]}")
        signature_counts[source] = overlap
    return signature_counts


def main(argv=None):
    from audit import audit
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--output-dir",type=Path,default=HERE / "data")
    a = parser.parse_args(argv)
    output = a.output_dir.resolve()
    if not output.is_relative_to(HERE) or output == HERE:
        parser.error("output directory must be a child of scope_revision_v1")
    rng = random.Random(a.seed)
    by_split = {s: make_split(s,rng) for s in SPLITS}
    files = {}
    for split, eps in by_split.items():
        name = f"{split}.jsonl"
        p = output / name
        write(p,"".join(json.dumps(e,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n"
                        for e in eps))
        files[name] = {"sha256": digest(p), "episodes": len(eps),
                       "categories": dict(Counter(x["gold"]["category"] for e in eps for x in e["events"]))}
    sample = output.parent / "samples.md"
    write(sample,markdown_samples(by_split,a.seed))
    write_json(output/"audit.json",audit(output))
    files["audit.json"] = {"sha256":digest(output/"audit.json")}
    files["../samples.md"] = {"sha256":digest(sample)}
    write_json(output/"manifest.json",{"seed":a.seed,"format":"scope-memory-v1","files":files})
    print("Built",", ".join(f"{s}={len(eps)}" for s,eps in by_split.items()),
          "episodes with seed",a.seed,flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
