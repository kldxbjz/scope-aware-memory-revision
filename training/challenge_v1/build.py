"""Challenge set v1 (protocol 1.2): hand-written episodes for structure-heavy cases that the v1.1 corpus leaves out.

  python3 training/challenge_v1/build.py               # write data/challenge.jsonl, data/manifest.json, samples.md
  python3 training/challenge_v1/build.py --check       # rebuild in memory and compare byte for byte with those files
  python3 training/challenge_v1/build.py --only dense  # check one episodes/ module and print it; writes nothing

The episodes are written by hand in episodes/<stressor>.py (format in spec.py). This script computes the gold states,
probe answers, options and ids, replays every episode with scope_memory.protocol.replay_gold and runs the extra checks
listed in README.md. Standard library only.
"""
import argparse
import calendar
import copy
import hashlib
import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True  # the episode modules are data; leave no caches next to them
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

from scope_memory.protocol import (CATEGORIES, PROBE_TYPES, QA_GROUP_OF, covers, norm, oracle_answer,  # noqa: E402
                                   read_episodes, replay_gold)
from spec import STRESSORS  # noqa: E402

V11 = ROOT / "training" / "scope_revision_v1" / "data"
# protocol.EXAMPLE_EVENT, shown to both policies in their instructions; no episode may use it
INSTRUCTION_EXAMPLE = ("drink order", "green tea", "at the office", "black coffee")
# wording that states a labelling rule or names a data field (docs/data-generation-prompt.md, quality rule 1)
LABEL_PHRASES = ("this is an exception", "an exception to", "treat this as", "treat it as", "as the default",
                 "everything else stays", "stays as it was", "won't guess", "scope_key", "state_after", "category",
                 "memory record", "general preference")
CHANGE_CATEGORY = {"general": "general_update", "add": "scoped_exception", "revise": "exception_revision",
                   "retire": "exception_retirement"}


def hid(prefix, *parts):
    return prefix + hashlib.sha256("/".join(parts).encode("utf-8")).hexdigest()[:20]


def month_day(date):
    year, month, day = (int(x) for x in date.split("-"))
    return f"{calendar.month_name[month]} {day}"


def load_specs(only=None):
    """(module stem, spec) pairs in STRESSORS order, then in list order."""
    out = []
    for stem in STRESSORS:
        path = HERE / "episodes" / f"{stem}.py"
        if not path.exists() or (only and stem != only):
            continue
        module_spec = importlib.util.spec_from_file_location(f"challenge_{stem}", path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        out += [(stem, spec) for spec in module.EPISODES]
    return out


def catalog_of(spec_attribute):
    return {"attribute": spec_attribute["attribute"], "options": list(spec_attribute["options"]),
            "value_aliases": {k: list(v) for k, v in spec_attribute.get("value_aliases", {}).items()},
            "scopes": {key: {"scope": phrase, "aliases": list(aliases)}
                       for key, (phrase, aliases) in spec_attribute["scopes"].items()}}


def apply_change(state, change):
    after = copy.deepcopy(state)
    if change is None:
        return after
    kind, attribute = change[0], change[1]
    if kind == "general":
        after[attribute]["general"] = change[2]
    elif kind in ("add", "revise"):
        after[attribute]["exceptions"][change[2]] = {"value": change[3], "validity": dict(change[4])}
    elif kind == "retire":
        del after[attribute]["exceptions"][change[2]]
    else:
        raise ValueError(f"unknown change {change!r}")
    return after


def pick_options(gold, attribute, key, state, history, catalog, probe_id):
    """Gold plus the three most confusable other values, in a fixed order: earlier values of the probed situation
    (latest first), the general value, the other active exceptions, earlier general values, the rest of the catalog."""
    entry = state[attribute]
    order = [gold, *reversed(history.get((attribute, key), [])), entry["general"],
             *(exc["value"] for _, exc in sorted(entry["exceptions"].items())),
             *reversed(history.get((attribute, None), [])), *catalog["options"]]
    picked = []
    for value in order:
        if value not in picked:
            picked.append(value)
    picked = picked[:4]
    random.Random(int(hashlib.sha256(probe_id.encode("utf-8")).hexdigest(), 16)).shuffle(picked)
    return picked


def build_episode(stem, spec, index):
    episode_id = f"ch-{index:04d}"
    attributes = [catalog_of(a) for a in spec["attributes"]]
    catalogs = {a["attribute"]: a for a in attributes}
    state = {attribute: {"general": general, "exceptions": {k: {"value": v, "validity": dict(val)}
                                                             for k, (v, val) in exceptions.items()}}
             for attribute, (general, exceptions) in spec["initial"].items()}
    initial = copy.deepcopy(state)
    history = {}  # (attribute, scope key or None) -> values it held before, oldest first
    events, probes = [], []
    for i, ev in enumerate(spec["events"], 1):
        event_id = hid("e", episode_id, f"event{i}")
        change, category = ev.get("change"), ev["category"]
        after = apply_change(state, change)
        for attribute in state:
            if state[attribute]["general"] != after[attribute]["general"]:
                history.setdefault((attribute, None), []).append(state[attribute]["general"])
            for key, exc in state[attribute]["exceptions"].items():
                if after[attribute]["exceptions"].get(key, {}).get("value") != exc["value"]:
                    history.setdefault((attribute, key), []).append(exc["value"])
        dialogue = [{"role": "user" if j % 2 == 0 else "assistant", "content": text}
                    for j, text in enumerate(ev["dialogue"])]
        note = ev.get("note") or (f"{category}: {change!r}" if change else category)
        events.append({"event_id": event_id, "date": ev["date"], "dialogue": dialogue,
                       "gold": {"category": category, "decision": "clarify" if category == "clarify" else "resolved",
                                "state_after": after, "evidence_message": ev["evidence"], "rationale": note}})
        default_attribute = change[1] if change else (spec["attributes"][0]["attribute"]
                                                      if len(spec["attributes"]) == 1 else None)
        for j, item in enumerate(ev.get("probes", []), 1):
            if isinstance(item, dict):
                ptype, key = item["type"], item.get("key")
                attribute, date = item.get("attribute", default_attribute), item.get("date", ev["date"])
            else:
                (ptype, key), attribute, date = item, default_attribute, ev["date"]
            if attribute is None:
                raise ValueError(f"{spec['name']} event {i}: probe {j} must name its attribute")
            catalog = catalogs[attribute]
            probe_id = hid("p", episode_id, f"event{i}", f"probe{j}")
            phrase = catalog["scopes"][key]["scope"] if key else "an ordinary occasion"
            probe = {"probe_id": probe_id, "after_event": event_id, "attribute": attribute,
                     "question": f"It is {month_day(date)} and the situation is {phrase}. "
                                 f"Which {attribute} would fit the preference?",
                     "date": date, "situation_scope_keys": [key] if key else [],
                     "category": QA_GROUP_OF[category], "probe_type": ptype}
            gold = oracle_answer(after, probe)
            probe["options"] = pick_options(gold, attribute, key, after, history, catalog, probe_id)
            probe["gold"] = gold
            probes.append(probe)
        state = after
    return {"episode_id": episode_id, "split": "challenge", "family": f"challenge-{stem}-{spec['name']}",
            "contrast_group": None, "attributes": attributes, "initial_state": initial, "events": events,
            "probes": probes}


def v11_strings():
    """Normalized attribute names, values, scope phrases and aliases of the v1.1 corpus (all splits)."""
    strings = {norm(s) for s in INSTRUCTION_EXAMPLE}
    for split in ("train", "dev", "test"):
        path = V11 / f"{split}.jsonl"
        if not path.exists():
            continue
        for episode in read_episodes(path):
            for a in episode["attributes"]:
                strings.add(norm(a["attribute"]))
                strings.update(norm(o) for o in a["options"])
                strings.update(norm(x) for xs in a.get("value_aliases", {}).values() for x in xs)
                for s in a["scopes"].values():
                    strings.add(norm(s["scope"]))
                    strings.update(norm(x) for x in s.get("aliases", []))
    return strings


def catalog_strings(catalog):
    yield catalog["attribute"]
    yield from catalog["options"]
    for aliases in catalog.get("value_aliases", {}).values():
        yield from aliases
    for scope in catalog["scopes"].values():
        yield scope["scope"]
        yield from scope["aliases"]


def check_episode(stem, spec, episode, used):
    """Checks beyond replay_gold (README.md); returns a list of problems."""
    problems = []
    name = f"{episode['episode_id']} ({stem}/{spec['name']})"
    if spec.get("stressor") != stem:
        problems.append(f"{name}: stressor {spec.get('stressor')!r} is not the module's {stem!r}")
    try:
        replay_gold(episode)
    except ValueError as exc:
        problems.append(f"{name}: replay_gold: {exc}")
    for catalog in episode["attributes"]:
        options = [norm(o) for o in catalog["options"]]
        if not 4 <= len(options) <= 6:
            problems.append(f"{name}: {catalog['attribute']!r} needs 4-6 options")
        if any(a != b and a in b for a in options for b in options):
            problems.append(f"{name}: an option of {catalog['attribute']!r} is part of another option")
        value_forms = options + [norm(x) for xs in catalog["value_aliases"].values() for x in xs]
        scope_forms = [norm(x) for s in catalog["scopes"].values() for x in [s["scope"], *s["aliases"]]]
        if len(set(value_forms)) != len(value_forms) or len(set(scope_forms)) != len(scope_forms):
            problems.append(f"{name}: {catalog['attribute']!r} repeats a value or situation form")
        for text in catalog_strings(catalog):
            if norm(text) in used["v11"]:
                problems.append(f"{name}: {text!r} also occurs in the v1.1 corpus or the instruction example")
        used["attributes"][catalog["attribute"]] += 1
    dates = [e["date"] for e in episode["events"]]
    state = episode["initial_state"]
    for i, event in enumerate(episode["events"]):
        change = spec["events"][i].get("change")
        if change and change[0] in ("add", "revise", "general"):
            entry = state[change[1]]
            value = change[2] if change[0] == "general" else change[3]
            others = [x["value"] for k, x in entry["exceptions"].items() if change[0] == "general" or k != change[2]]
            if change[0] != "general" and value == entry["general"]:
                problems.append(f"{name} {event['event_id']}: a situation set to the general value is a retirement")
            if change[0] == "general" and value in others:
                problems.append(f"{name} {event['event_id']}: new general value equals an exception (ambiguous)")
        state = event["gold"]["state_after"]
        n = len(event["dialogue"])
        if n not in (3, 5, 7):
            problems.append(f"{name} {event['event_id']}: 3, 5 or 7 messages (the v1.1 shape), not {n}")
        for message in event["dialogue"]:
            text = norm(message["content"])
            for phrase in LABEL_PHRASES:
                if phrase in text:
                    problems.append(f"{name} {event['event_id']}: label wording {phrase!r}")
        change = spec["events"][i].get("change")
        expected = CHANGE_CATEGORY[change[0]] if change else None
        if expected and event["gold"]["category"] != expected:
            problems.append(f"{name} {event['event_id']}: change {change[0]} needs {expected}")
        if not change and event["gold"]["category"] not in ("stable_preference", "clarify"):
            problems.append(f"{name} {event['event_id']}: no change needs stable_preference or clarify")
    states = {e["event_id"]: e["gold"]["state_after"] for e in episode["events"]}
    order = {e["event_id"]: i for i, e in enumerate(episode["events"])}
    seen = set()
    for probe in episode["probes"]:
        i = order[probe["after_event"]]
        if probe["date"] < dates[i] or (i + 1 < len(dates) and probe["date"] >= dates[i + 1]):
            problems.append(f"{name} {probe['probe_id']}: date must fall between its event and the next one")
        if len(set(probe["options"])) != 4:
            problems.append(f"{name} {probe['probe_id']}: needs four different options")
        if probe["probe_type"] not in PROBE_TYPES:
            problems.append(f"{name} {probe['probe_id']}: bad probe type")
        entry = states[probe["after_event"]][probe["attribute"]]
        windowed = [k for k in probe["situation_scope_keys"]
                    if k in entry["exceptions"] and entry["exceptions"][k]["validity"]["kind"] == "window"]
        outside = any(not covers(entry["exceptions"][k]["validity"], probe["date"]) for k in windowed)
        if outside != (probe["probe_type"] == "boundary"):
            problems.append(f"{name} {probe['probe_id']}: boundary probes are exactly the dates outside a window")
        signature = (probe["after_event"], probe["attribute"], tuple(probe["situation_scope_keys"]), probe["date"])
        if signature in seen:
            problems.append(f"{name} {probe['probe_id']}: the same question twice")
        seen.add(signature)
    if not episode["probes"]:
        problems.append(f"{name}: no probes")
    return problems


def max_exceptions(episode):
    states = [episode["initial_state"]] + [e["gold"]["state_after"] for e in episode["events"]]
    return max(len(s[a]["exceptions"]) for s in states for a in s)


def manifest(episodes, data_bytes):
    events = [e for ep in episodes for e in ep["events"]]
    probes = [p for ep in episodes for p in ep["probes"]]
    created = Counter()
    for ep in episodes:
        state = ep["initial_state"]
        for event in ep["events"]:
            for a, entry in event["gold"]["state_after"].items():
                for k, exc in entry["exceptions"].items():
                    if state[a]["exceptions"].get(k) != exc:
                        created[exc["validity"]["kind"]] += 1
            state = event["gold"]["state_after"]
    return {"file": "data/challenge.jsonl", "sha256": hashlib.sha256(data_bytes).hexdigest(),
            "episodes": len(episodes), "events": len(events), "probes": len(probes),
            "episodes_per_stressor": dict(Counter(ep["family"].split("-")[1] for ep in episodes)),
            "two_attribute_episodes": sum(len(ep["attributes"]) == 2 for ep in episodes),
            "events_per_category": {c: sum(e["gold"]["category"] == c for e in events) for c in CATEGORIES},
            "probes_per_qa_group": dict(sorted(Counter(p["category"] for p in probes).items())),
            "probes_per_type": {t: sum(p["probe_type"] == t for p in probes) for t in PROBE_TYPES},
            "probes_per_stressor": dict(Counter(ep["family"].split("-")[1] for ep in episodes for _ in ep["probes"])),
            "written_exception_validity": dict(sorted(created.items())),
            "max_active_exceptions_per_attribute": dict(sorted(Counter(map(max_exceptions, episodes)).items()))}


def describe_validity(v):
    return {"persistent": "persistent", "open": "open (temporary, no end)"}.get(v["kind"]) or f"{v['from']} to {v['to']}"


def render(episode):
    """Readable version of one episode for the team's review (samples.md)."""
    lines = [f"## {episode['episode_id']} · {episode['family']}", ""]
    for c in episode["attributes"]:
        aliases = "; ".join(f"{o} ({', '.join(c['value_aliases'].get(o, [])) or '-'})" for o in c["options"])
        scopes = "; ".join(f"{k} = {s['scope']} ({', '.join(s['aliases']) or '-'})" for k, s in c["scopes"].items())
        lines += [f"- **{c['attribute']}** — options (aliases): {aliases}", f"  - situations: {scopes}"]
    for a, entry in episode["initial_state"].items():
        exc = "; ".join(f"{k}: {x['value']}, {describe_validity(x['validity'])}" for k, x in entry["exceptions"].items())
        lines.append(f"- initial {a}: general {entry['general']}" + (f"; {exc}" if exc else ""))
    state = episode["initial_state"]
    for event in episode["events"]:
        gold = event["gold"]
        lines += ["", f"### {event['date']} · {gold['category']} · evidence message {gold['evidence_message']}", ""]
        lines += [f"{'U' if m['role'] == 'user' else 'A'}: {m['content']}  " for m in event["dialogue"]]
        changed = []
        for a, entry in gold["state_after"].items():
            if entry["general"] != state[a]["general"]:
                changed.append(f"{a} general → {entry['general']}")
            for k in sorted(set(entry["exceptions"]) | set(state[a]["exceptions"])):
                new, old = entry["exceptions"].get(k), state[a]["exceptions"].get(k)
                if new != old:
                    changed.append(f"{a} [{k}] → " + (f"{new['value']}, {describe_validity(new['validity'])}"
                                                      if new else "retired (follows the general value)"))
        lines += ["", "Gold: " + ("; ".join(changed) or "no change") + f". Note: {gold['rationale']}"]
        for p in episode["probes"]:
            if p["after_event"] == event["event_id"]:
                where = p["situation_scope_keys"][0] if p["situation_scope_keys"] else "ordinary"
                lines.append(f"- probe {p['probe_type']}, {p['attribute']} [{where}] on {p['date']}: **{p['gold']}** "
                             f"(options: {' | '.join(p['options'])})")
        state = gold["state_after"]
    return "\n".join(lines) + "\n"


def build(only=None):
    specs = load_specs(only)
    names = Counter(spec["name"] for _, spec in specs)
    problems = [f"episode name {n!r} used {k} times" for n, k in names.items() if k > 1]
    used = {"v11": v11_strings(), "attributes": Counter()}
    episodes = []
    for index, (stem, spec) in enumerate(specs, 1):
        try:
            episode = build_episode(stem, spec, index)
        except (KeyError, ValueError, TypeError) as exc:
            problems.append(f"{stem}/{spec.get('name')}: cannot build ({exc!r})")
            continue
        episodes.append(episode)
        problems += check_episode(stem, spec, episode, used)
    problems += [f"attribute {a!r} used in {k} episodes" for a, k in used["attributes"].items() if k > 1]
    return episodes, problems


def outputs(episodes):
    data = "".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in episodes).encode("utf-8")
    man = (json.dumps(manifest(episodes, data), ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    head = ("# Challenge set v1: all episodes\n\nGenerated by `build.py` from `episodes/`; gold states, answers and "
            "options are computed, the dialogues and changes are hand-written. Review copy for the team.\n\n")
    samples = (head + "\n".join(render(e) for e in episodes)).encode("utf-8")
    return {HERE / "data" / "challenge.jsonl": data, HERE / "data" / "manifest.json": man, HERE / "samples.md": samples}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="compare a rebuild with the files on disk")
    parser.add_argument("--only", choices=STRESSORS, help="check and print one module; write nothing")
    args = parser.parse_args(argv)
    episodes, problems = build(args.only)
    for p in problems:
        print("PROBLEM", p)
    if args.only:
        for e in episodes:
            print(render(e))
        print(f"{len(episodes)} episodes, {sum(len(e['probes']) for e in episodes)} probes, {len(problems)} problems")
        return 1 if problems else 0
    if problems:
        return 1
    files = outputs(episodes)
    if args.check:
        stale = [str(p.relative_to(HERE)) for p, data in files.items() if not p.exists() or p.read_bytes() != data]
        print("stale: " + ", ".join(stale) if stale else f"up to date: {len(episodes)} episodes")
        return 1 if stale else 0
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(json.dumps(manifest(episodes, files[HERE / "data" / "challenge.jsonl"]), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
