"""Analyses of finished runs for the report (docs/analysis.md).

  python3 -m scope_memory.analysis report --sft RUN [RUN ...] --zero-shot RUN --six-shot RUN --gold RUN --noop RUN
  python3 -m scope_memory.analysis paired --a RUN [RUN ...] --arm-a scope --b RUN [RUN ...] --arm-b crud
  python3 -m scope_memory.analysis memory-classes RUN [RUN ...]
  python3 -m scope_memory.analysis structure RUN [RUN ...]
  python3 -m scope_memory.analysis error-sample RUN --arm scope --n 40 --seed 0 --out DIR
  python3 -m scope_memory.analysis label-sample DATA [DATA ...] --per-category 5 --seed 0 --out DIR
  python3 -m scope_memory.analysis agreement --labels FILE FILE [--key KEY]

A RUN is a directory written by training/sft/baseline.sbatch: episodes.jsonl, trajectories.jsonl, answers.jsonl and,
for policy runs, predictions_<arm>.jsonl. Answer Agent correctness is the primary measure; everything read with the
rule readers is a diagnostic. Intervals are 95% episode-bootstrap intervals: an episode is resampled together with
all its probes and all seeds. Standard library only.
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from .evaluate import _ci, _read_keyed, gold_policy, parse_output, rollout, score_rollouts
from .protocol import (ARMS, CATEGORIES, CRUD_EXCEPTION, CRUD_GENERAL, GENERAL, PERSISTENT, PROBE_TYPES, QA_GROUPS,
                       _attribute_lookup, canonical_state, canonical_value, catalogs_of, crud_sentence, norm,
                       read_episodes, replay_gold, scope_forms, scope_key, sft_rows, value_forms)

GROUPS = ("all", "all_but_boundary") + QA_GROUPS + tuple(f"type_{t}" for t in PROBE_TYPES)
CLASSES = ("matches_gold", "same_structure", "different_structure", "unreadable")
ERROR_SOURCES = ("action", "executor_rejection", "reader_matching", "answer_reasoning", "data", "other")


# ---------------------------------------------------------------- loading and pooling

def load_run(path):
    """Episodes, trajectories by (episode, arm) and Answer Agent scores by probe id of one finished run."""
    path = Path(path)
    episodes = read_episodes(path / "episodes.jsonl")
    trajectories = [json.loads(line) for line in (path / "trajectories.jsonl").read_text(encoding="utf-8").splitlines()
                    if line.strip()]
    scored = score_rollouts(episodes, trajectories, _read_keyed(path / "answers.jsonl", "answer"))
    return {"path": str(path), "episodes": episodes,
            "trajectories": {(t["episode_id"], t["arm"]): t for t in trajectories},
            "scored": {s["id"]: s for s in scored}}


def stressor_of(episode):
    """The stressor of a challenge-set episode (family challenge-<stressor>-<name>), otherwise None."""
    family = str(episode.get("family") or "")
    return family.split("-")[1] if family.startswith("challenge-") and family.count("-") >= 2 else None


def probe_info(episodes):
    """'<episode>/<probe>' -> episode, QA group, probe type and challenge-set stressor (None outside it)."""
    return {f"{e['episode_id']}/{p['probe_id']}": {"episode_id": e["episode_id"], "qa_group": p["category"],
                                                   "probe_type": p["probe_type"], "stressor": stressor_of(e)}
            for e in episodes for p in e.get("probes", [])}


def groups_for(info):
    """GROUPS plus a stressor_<name> group for each challenge-set stressor among the probes."""
    return GROUPS + tuple(f"stressor_{s}" for s in sorted({i["stressor"] for i in info.values() if i.get("stressor")}))


def correctness(runs, arm):
    """Per probe ('<episode>/<probe>'), the share of the runs (seeds) whose Answer Agent answered it correctly."""
    tables = [{key.rsplit("/", 1)[0]: float(s["correct"]) for key, s in run["scored"].items() if s["arm"] == arm}
              for run in runs]
    keys = set(tables[0]) if tables else set()
    if not keys or any(set(t) != keys for t in tables[1:]):
        raise ValueError(f"the runs cover different probes for arm {arm}")
    return {k: sum(t[k] for t in tables) / len(tables) for k in keys}


def _in_group(info, group):
    if group == "all":
        return True
    if group == "all_but_boundary":
        return info["probe_type"] != "boundary"
    if group.startswith("type_"):
        return info["probe_type"] == group[len("type_"):]
    if group.startswith("stressor_"):
        return info.get("stressor") == group[len("stressor_"):]
    return info["qa_group"] == group


def _picks(episodes, bootstrap, seed):
    """The same resampling as scope_memory.evaluate: episode names drawn with replacement."""
    names = sorted(episodes)
    rng = random.Random(seed)
    return [[names[rng.randrange(len(names))] for _ in names] for _ in range(bootstrap)]


def _summarize_cells(cells, picks):
    """cells: episode -> [sum of a, sum of b, probes]. Means of a, b and a - b with an interval for a - b."""
    n = sum(c[2] for c in cells.values())
    if not n:
        return None
    sum_a, sum_b = sum(c[0] for c in cells.values()), sum(c[1] for c in cells.values())
    gap = {e: c[0] - c[1] for e, c in cells.items()}
    size = {e: c[2] for e, c in cells.items()}
    diffs = []
    for pick in picks:
        m = sum(size.get(e, 0) for e in pick)
        if m:
            diffs.append(sum(gap.get(e, 0.0) for e in pick) / m)
    return {"probes": n, "a": round(sum_a / n, 4), "b": round(sum_b / n, 4), "difference": round((sum_a - sum_b) / n, 4),
            "ci95": _ci(diffs), "sum_difference": round(sum_a - sum_b, 2)}


def paired(a, b, info, groups=None, bootstrap=2000, seed=0):
    """Means of a and b (probe -> value in [0, 1]) and of a - b in each group (default: groups_for(info)), with
    episode-bootstrap intervals for the difference. a, b and info must cover the same probes."""
    if set(a) != set(info) or set(b) != set(info):
        raise ValueError("a, b and the probe table cover different probes")
    groups = groups or groups_for(info)
    picks = _picks({i["episode_id"] for i in info.values()}, bootstrap, seed)
    out = {}
    for group in groups:
        cells = defaultdict(lambda: [0.0, 0.0, 0])
        for key, i in info.items():
            if _in_group(i, group):
                cell = cells[i["episode_id"]]
                cell[0] += a[key]
                cell[1] += b[key]
                cell[2] += 1
        summary = _summarize_cells(dict(cells), picks)
        if summary:
            out[group] = summary
    return out


def accuracy(a, info, groups=None, bootstrap=2000, seed=0):
    """Mean of a in each group with an episode-bootstrap interval."""
    out = {}
    for group, s in paired(a, {k: 0.0 for k in a}, info, groups, bootstrap, seed).items():
        out[group] = {"probes": s["probes"], "accuracy": s["a"], "ci95": s["ci95"]}
    return out


def report(conditions, bootstrap=2000, seed=0):
    """Main table: accuracy per condition and arm, scope minus CRUD per condition, H1 (SFT scope minus SFT CRUD) and H2
    (SFT minus each prompt baseline, per arm). conditions: name -> loaded runs (several runs = seeds, pooled)."""
    info = None
    tables = {}
    for name, runs in conditions.items():
        if not runs:
            continue
        mine = probe_info(runs[0]["episodes"])
        if info is not None and mine != info:
            raise ValueError(f"condition {name} covers other probes")
        info = mine
        tables[name] = {arm: correctness(runs, arm) for arm in ARMS}
    out = {"conditions": {name: len(runs) for name, runs in conditions.items() if runs}, "accuracy": {},
           "scope_minus_crud": {}}
    for name, table in tables.items():
        out["accuracy"][name] = {arm: accuracy(table[arm], info, bootstrap=bootstrap, seed=seed) for arm in ARMS}
        out["scope_minus_crud"][name] = paired(table["scope"], table["crud"], info, bootstrap=bootstrap, seed=seed)
    if "sft" in tables:
        out["h1_sft_scope_minus_crud"] = out["scope_minus_crud"]["sft"]
        out["h2_sft_minus_prompt"] = {arm: {f"sft_minus_{base}": paired(tables["sft"][arm], tables[base][arm], info,
                                                                         bootstrap=bootstrap, seed=seed)
                                            for base in ("zero_shot", "six_shot") if base in tables}
                                      for arm in ARMS}
    return out


# ---------------------------------------------------------------- memory against gold (rule readers, diagnostic)

def _slots(view, arm, catalogs, attribute):
    """(slot, value, validity) for each record of `attribute`, slot None for the general record and a scope key
    otherwise; None when a record that may belong to the attribute does not map to the catalog."""
    catalog = catalogs[attribute]
    slots = []
    for record in view:
        if arm == "scope":
            if norm(record["attribute"]) != norm(attribute):
                continue
            if norm(record["scope"]) == GENERAL:
                slot, validity = None, PERSISTENT
            else:
                slot, validity = scope_key(catalog, record["scope"]), record["validity"]
                if slot is None:
                    return None
            slots.append((slot, canonical_value(catalog, record["value"]), dict(validity)))
            continue
        text = " ".join(record["text"].split())
        match = CRUD_EXCEPTION.fullmatch(text) or CRUD_GENERAL.fullmatch(text)
        owner = _attribute_lookup(catalogs, match["attribute"]) if match else None
        if owner is None:  # text the rule reader cannot place: unreadable for the attributes it may be about
            mentioned = [a for a in catalogs if norm(a) in norm(text)]
            if not mentioned or attribute in mentioned:
                return None
            continue
        if owner != attribute:
            continue
        if match.re is CRUD_EXCEPTION:
            slot = scope_key(catalog, match["scope"])
            if slot is None:
                return None
            if match["start"]:
                validity = {"kind": "window", "from": match["start"], "to": match["end"]}
            else:
                validity = {"kind": "open"} if match["open"] else dict(PERSISTENT)
        else:
            slot, validity = None, dict(PERSISTENT)
        slots.append((slot, canonical_value(catalog, match["value"]), validity))
    return slots


def attribute_class(view, arm, catalogs, attribute, gold_entry):
    """How one attribute's memory compares with its gold state, read with the arm's rule reader: matches_gold;
    same_structure (the same records and validity, some value differs); different_structure (records or validity
    differ, duplicates included); unreadable (a record does not map to the catalog)."""
    slots = _slots(view, arm, catalogs, attribute)
    if slots is None:
        return "unreadable"
    gold = {None: (gold_entry["general"], PERSISTENT)}
    gold.update({key: (exc["value"], exc["validity"]) for key, exc in gold_entry["exceptions"].items()})
    mine = {}
    for slot, value, validity in slots:
        if slot in mine:
            return "different_structure"
        mine[slot] = (value, validity)
    if set(mine) != set(gold) or any(mine[s][1] != gold[s][1] for s in gold):
        return "different_structure"
    return "matches_gold" if all(mine[s][0] == gold[s][0] for s in gold) else "same_structure"


def memory_classes(runs, bootstrap=2000, seed=0):
    """Each probe's memory class per arm (attribute_class), QA accuracy per class, and the paired scope-minus-CRUD
    difference split by either arm's class: where the gap between the arms sits. Rule-reader diagnostic."""
    rows = []
    for run in runs:
        for e in run["episodes"]:
            catalogs = catalogs_of(e)
            gold = {ev["event_id"]: canonical_state(ev["gold"]["state_after"], catalogs) for ev in e["events"]}
            for p in e.get("probes", []):
                row = {"episode_id": e["episode_id"]}
                for arm in ARMS:
                    view = run["trajectories"][(e["episode_id"], arm)]["snapshots"][p["after_event"]]
                    row[arm] = (attribute_class(view, arm, catalogs, p["attribute"],
                                                gold[p["after_event"]][p["attribute"]]),
                                float(run["scored"][f"{e['episode_id']}/{p['probe_id']}/{arm}"]["correct"]))
                rows.append(row)
    picks = _picks({r["episode_id"] for r in rows}, bootstrap, seed)
    out = {"runs": len(runs), "probes": len(rows), "classes": {}, "paired_by_class": {}}
    for arm in ARMS:
        counts = Counter(r[arm][0] for r in rows)
        out["classes"][arm] = {c: {"probes": counts[c], "share": round(counts[c] / len(rows), 4),
                                   "accuracy": round(sum(r[arm][1] for r in rows if r[arm][0] == c) / counts[c], 4)}
                               for c in CLASSES if counts[c]}
        split = {}
        for c in CLASSES:
            cells = defaultdict(lambda: [0.0, 0.0, 0])
            for r in rows:
                if r[arm][0] == c:
                    cell = cells[r["episode_id"]]
                    cell[0] += r["scope"][1]
                    cell[1] += r["crud"][1]
                    cell[2] += 1
            summary = _summarize_cells(dict(cells), picks)
            if summary:
                split[c] = {"probes": summary["probes"], "scope": summary["a"], "crud": summary["b"],
                            "difference": summary["difference"], "ci95": summary["ci95"],
                            "gap_probes": summary["sum_difference"]}
        out["paired_by_class"][f"by_{arm}_class"] = split
    return out


# ---------------------------------------------------------------- teacher-forced structure (diagnostic)

def scope_structure(output):
    """Operations with their targets, validity kinds and EXCEPTION_TO targets; written strings are left out."""
    actions = output.get("actions") if isinstance(output, dict) else None
    shape = []
    for a in actions if isinstance(actions, list) else []:
        if not isinstance(a, dict):
            continue
        op = a.get("operation")
        writes = op in ("ADD", "REVISE")
        validity = a.get("validity") if isinstance(a.get("validity"), dict) else {}
        relations = a.get("relations") if isinstance(a.get("relations"), list) else []
        shape.append((str(op), str(a.get("target_id")) if op in ("REVISE", "RETIRE") else None,
                      str(validity.get("kind")) if writes else None,
                      tuple(sorted(str(r.get("target")) for r in relations
                                   if isinstance(r, dict) and r.get("type") == "EXCEPTION_TO")) if writes else None))
    return sorted(shape, key=repr)


def crud_structure(output):
    """Operations with their target ids; texts are left out."""
    operations = output.get("operations") if isinstance(output, dict) else None
    return sorted(((str(o.get("op")), str(o.get("id")) if o.get("op") in ("UPDATE", "DELETE") else None)
                   for o in (operations if isinstance(operations, list) else []) if isinstance(o, dict)), key=repr)


STRUCTURE = {"scope": scope_structure, "crud": crud_structure}


def _short(shape, arm):
    return tuple(f"{s[0]}:{s[2]}" if arm == "scope" and s[2] else s[0] for s in shape)


def _written(output, arm):
    """(field, text) for each value and situation an output writes; CRUD texts are split with the CRUD sentences."""
    if arm == "scope":
        for a in output.get("actions") or []:
            if isinstance(a, dict) and a.get("operation") in ("ADD", "REVISE"):
                yield "value", str(a.get("value"))
                if norm(str(a.get("scope"))) != GENERAL:
                    yield "situation", str(a.get("scope"))
        return
    for o in output.get("operations") or []:
        if isinstance(o, dict) and o.get("op") in ("ADD", "UPDATE"):
            text = " ".join(str(o.get("text")).split())
            match = CRUD_EXCEPTION.fullmatch(text) or CRUD_GENERAL.fullmatch(text)
            if match is None:
                yield "sentence", None
                continue
            yield "value", match["value"]
            if match.re is CRUD_EXCEPTION:
                yield "situation", match["scope"]


def _listed(catalogs):
    values = {norm(f) for c in catalogs.values() for o in c["options"] for f in value_forms(c, o)}
    situations = {norm(f) for c in catalogs.values() for k in c["scopes"] for f in scope_forms(c, k)}
    return {"value": values, "situation": situations}


def structure(runs, top=12):
    """Teacher-forced diagnostics per arm: how often the operation structure matches gold (by category), the most common
    mismatches (gold -> predicted), and whether written values and situations are listed forms (catalog name or alias)
    or other text. Runs without predictions_<arm>.jsonl are skipped for that arm."""
    match = {arm: defaultdict(lambda: [0, 0]) for arm in ARMS}
    patterns = {arm: Counter() for arm in ARMS}
    forms = {arm: Counter() for arm in ARMS}
    for run in runs:
        predictions = {}
        for arm in ARMS:
            path = Path(run["path"]) / f"predictions_{arm}.jsonl"
            if path.exists():
                predictions.update(_read_keyed(path, "completion"))
        for e in run["episodes"]:
            listed = _listed(catalogs_of(e))
            for row in sft_rows(e):
                if row["id"] not in predictions:
                    continue
                arm, shape = row["arm"], STRUCTURE[row["arm"]]
                gold, _ = parse_output(row["completion"])
                out, _ = parse_output(predictions[row["id"]])
                ok = out is not None and shape(out) == shape(gold)
                cell = match[arm][row["category"]]
                cell[0] += ok
                cell[1] += 1
                if not ok:
                    patterns[arm][(row["category"], _short(shape(gold), arm),
                                   _short(shape(out), arm) if out is not None else "unparsed")] += 1
                if out is not None:
                    for field, text in _written(out, arm):
                        kind = "unparsed" if text is None else "listed" if norm(text) in listed[field] else "other"
                        forms[arm][f"{field}:{kind}"] += 1
    report_ = {}
    for arm in ARMS:
        total = [sum(c[0] for c in match[arm].values()), sum(c[1] for c in match[arm].values())]
        if not total[1]:
            continue
        report_[arm] = {"structure_matches_gold": {"count": total[0], "of": total[1], "rate": round(total[0] / total[1], 4),
                                                   "by_category": {c: f"{v[0]}/{v[1]}" for c, v in sorted(match[arm].items())}},
                        "top_mismatches": [{"count": n, "category": k[0], "gold": list(k[1]),
                                            "predicted": k[2] if isinstance(k[2], str) else list(k[2])}
                                           for k, n in patterns[arm].most_common(top)],
                        "written_forms": dict(sorted(forms[arm].items()))}
    return report_


# ---------------------------------------------------------------- manual error analysis packet

def _gold_snapshots(episode, arm):
    return rollout(episode, arm, gold_policy([episode]))["snapshots"]


def error_sample(run, arm, n, seed):
    """n probes the Answer Agent got wrong for `arm`, drawn with random.Random(seed) from the sorted wrong probe ids,
    as packet items with everything an annotator needs to name the error source."""
    wrong = sorted(k for k, s in run["scored"].items() if s["arm"] == arm and not s["correct"])
    chosen = sorted(random.Random(seed).sample(wrong, min(n, len(wrong))))
    by_id = {e["episode_id"]: e for e in run["episodes"]}
    answers = {}
    path = Path(run["path"]) / "answers.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            answers[row["id"]] = row
    items = []
    for key in chosen:
        episode_id, probe_id, _ = key.split("/")
        e = by_id[episode_id]
        probe = next(p for p in e["probes"] if p["probe_id"] == probe_id)
        trajectory = run["trajectories"][(episode_id, arm)]
        steps = {s["event_id"]: s for s in trajectory["steps"]}
        gold_outputs = {s["event_id"]: s["outputs"][arm] for s in replay_gold(e)}
        events = []
        for ev in e["events"]:
            step = steps.get(ev["event_id"], {})
            events.append({"event_id": ev["event_id"], "date": ev["date"], "dialogue": ev["dialogue"],
                           "gold_category": ev["gold"]["category"], "gold_output": gold_outputs[ev["event_id"]],
                           "policy_output": step.get("completion"), "accepted": step.get("accepted"),
                           "rejection": step.get("reason")})
            if ev["event_id"] == probe["after_event"]:
                break
        items.append({"id": key, "qa_group": probe["category"], "probe_type": probe["probe_type"],
                      "date": probe["date"], "question": probe["question"], "options": probe["options"],
                      "gold": probe["gold"], "answer": run["scored"][key]["answer"],
                      "answer_agent_reply": answers.get(key, {}).get("raw"),
                      "memory": trajectory["snapshots"][probe["after_event"]],
                      "gold_memory": _gold_snapshots(e, arm)[probe["after_event"]], "events": events})
    return {"run": run["path"], "arm": arm, "wrong_probes": len(wrong), "sampled": len(items), "seed": seed,
            "items": items}


def _json_block(obj):
    return "```json\n" + json.dumps(obj, ensure_ascii=False, indent=1) + "\n```"


def error_packet_markdown(sample):
    lines = [f"# Error analysis packet: {sample['arm']} arm", "",
             f"Run `{sample['run']}`: {sample['sampled']} of {sample['wrong_probes']} wrong probes, sampled with seed "
             f"{sample['seed']}. Label every item in the labels file with one source from docs/analysis.md "
             f"({', '.join(ERROR_SOURCES)}) and a short note. Label alone first; compare afterwards.", ""]
    for n, item in enumerate(sample["items"], 1):
        lines += [f"## {n}. `{item['id']}` ({item['qa_group']}, {item['probe_type']} probe)", "",
                  f"- Question ({item['date']}): {item['question']}",
                  f"- Options: {' | '.join(item['options'])}",
                  f"- Gold: **{item['gold']}**; Answer Agent chose: **{item['answer']}**",
                  f"- Answer Agent reply: {json.dumps(item['answer_agent_reply'], ensure_ascii=False)}", "",
                  "Memory at the probe (this arm):", _json_block(item["memory"]), "",
                  "Gold memory at the probe (same format):", _json_block(item["gold_memory"]), "", "Events up to the probe:"]
        for ev in item["events"]:
            lines += ["", f"### `{ev['event_id']}` ({ev['date']}), gold category {ev['gold_category']}"]
            lines += [f"- {m['role']}: {m['content']}" for m in ev["dialogue"]]
            status = "accepted" if ev["accepted"] else f"REJECTED ({ev['rejection']})"
            lines += ["", f"Gold output: `{json.dumps(ev['gold_output'], ensure_ascii=False)}`",
                      f"Policy output ({status}): `{ev['policy_output']}`"]
        lines.append("")
    return "\n".join(lines) + "\n"


def label_template(ids, field, allowed):
    return {"annotator": "", "field": field, "allowed": list(allowed),
            "items": [{"id": i, field: "", "note": ""} for i in ids]}


# ---------------------------------------------------------------- label audit of the synthetic data

def label_sample(paths, per_category, seed):
    """per_category events of every category from each data file, drawn with random.Random(seed) and shown in a
    shuffled order under opaque ids; the key maps each id to (file, episode, event)."""
    rng = random.Random(seed)
    picked = []
    for path in paths:
        by_category = defaultdict(list)
        for e in read_episodes(path):
            state = e["initial_state"]
            for ev in e["events"]:
                by_category[ev["gold"]["category"]].append((str(path), e, ev, state))
                state = ev["gold"]["state_after"]
        for category in CATEGORIES:
            pool = sorted(by_category[category], key=lambda x: (x[1]["episode_id"], x[2]["event_id"]))
            picked += rng.sample(pool, min(per_category, len(pool)))
    rng.shuffle(picked)
    items, key = [], {}
    for n, (path, e, ev, state) in enumerate(picked, 1):
        item_id = f"L{n:03d}"
        catalogs = catalogs_of(e)
        memory = []
        for attribute, entry in state.items():
            memory.append(crud_sentence(attribute, None, entry["general"], PERSISTENT))
            memory += [crud_sentence(attribute, catalogs[attribute]["scopes"][k]["scope"], exc["value"], exc["validity"])
                       for k, exc in sorted(entry["exceptions"].items())]
        items.append({"id": item_id, "date": ev["date"], "memory": memory, "dialogue": ev["dialogue"]})
        key[item_id] = {"file": path, "episode_id": e["episode_id"], "event_id": ev["event_id"]}
    return items, key


CATEGORY_NOTES = {
    "general_update": "the usual (general) preference changes; situation-specific preferences stay",
    "scoped_exception": "a new preference for one situation (lasting, for dates, or for now)",
    "exception_revision": "an existing situation-specific preference changes its value or its dates",
    "exception_retirement": "an existing situation-specific preference is dropped, so that situation follows the "
                            "usual preference again",
    "stable_preference": "nothing to store: a one-off request, someone else's or a quoted preference, a hypothetical, "
                         "a rejected suggestion, or a restated preference",
    "clarify": "nothing to store yet: the user leaves open what should change or for how long",
}


def label_packet_markdown(items):
    lines = ["# Label audit packet", "",
             "For each item, read the stored preferences and the conversation, then choose the one category that "
             "describes what should change in the user's lasting preferences (protocol section 3). Label alone; do "
             "not look up the data files.", ""]
    lines += [f"- `{c}`: {CATEGORY_NOTES[c]}" for c in CATEGORIES]
    for item in items:
        lines += ["", f"## {item['id']} ({item['date']})", "", "Stored preferences:"]
        lines += [f"- {m}" for m in item["memory"]]
        lines += ["", "Conversation:"] + [f"- {m['role']}: {m['content']}" for m in item["dialogue"]]
    return "\n".join(lines) + "\n"


def _labels(path, field=None):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    field = field or data["field"]
    labels = {it["id"]: it[field] for it in data["items"] if it.get(field)}
    bad = sorted({v for v in labels.values()} - set(data["allowed"]))
    if bad:
        raise ValueError(f"{path}: labels outside the allowed set: {bad}")
    return data.get("annotator") or str(path), labels


def agreement(a, b):
    """Raw agreement and Cohen's kappa of two label tables over the items both labelled."""
    keys = sorted(set(a) & set(b))
    if not keys:
        return None
    n = len(keys)
    observed = sum(a[k] == b[k] for k in keys) / n
    count_a, count_b = Counter(a[k] for k in keys), Counter(b[k] for k in keys)
    expected = sum(count_a[x] * count_b[x] for x in set(count_a) | set(count_b)) / (n * n)
    kappa = 1.0 if expected == 1 else (observed - expected) / (1 - expected)
    return {"items": n, "agreement": round(observed, 4), "kappa": round(kappa, 4)}


def agreement_report(label_paths, key_path=None):
    """Label distribution per annotator, pairwise agreement and Cohen's kappa, and, with the label-audit key, each
    annotator's agreement with the gold category and the disagreements with gold."""
    tables = dict(_labels(p) for p in label_paths)
    out = {"annotators": {name: {"labelled": len(t), "labels": dict(Counter(t.values()))} for name, t in tables.items()},
           "pairwise": {}}
    names = sorted(tables)
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            out["pairwise"][f"{x} vs {y}"] = agreement(tables[x], tables[y])
    if key_path:
        key = json.loads(Path(key_path).read_text(encoding="utf-8"))
        gold = {}
        for path in sorted({v["file"] for v in key.values()}):
            events = {(e["episode_id"], ev["event_id"]): ev["gold"]["category"]
                      for e in read_episodes(path) for ev in e["events"]}
            gold.update({i: events[(v["episode_id"], v["event_id"])] for i, v in key.items() if v["file"] == path})
        out["against_gold"] = {name: {**agreement(t, gold),
                                      "disagreements": [{"id": i, "label": t[i], "gold": gold[i]}
                                                        for i in sorted(t) if t[i] != gold[i]]}
                               for name, t in tables.items() if set(t) & set(gold)}
    return out


# ---------------------------------------------------------------- command line

def _write(obj, out):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    print(text)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")


CONDITIONS = ("noop", "zero_shot", "six_shot", "sft", "gold")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyses of finished runs (docs/analysis.md).")
    sub = parser.add_subparsers(dest="command", required=True)
    reports = {}  # subcommands that print a JSON report; --out names a file for it
    reports["report"] = p = sub.add_parser("report", help="main table: accuracy per condition, scope minus CRUD, H1, H2")
    for name in CONDITIONS:
        p.add_argument(f"--{name.replace('_', '-')}", dest=name, nargs="+", default=[], metavar="RUN")
    reports["paired"] = p = sub.add_parser("paired", help="paired difference between two pooled conditions")
    p.add_argument("--a", nargs="+", required=True, metavar="RUN")
    p.add_argument("--arm-a", choices=ARMS, required=True)
    p.add_argument("--b", nargs="+", required=True, metavar="RUN")
    p.add_argument("--arm-b", choices=ARMS, required=True)
    for name in ("memory-classes", "structure"):
        reports[name] = p = sub.add_parser(name)
        p.add_argument("runs", nargs="+", metavar="RUN")
    reports["agreement"] = p = sub.add_parser("agreement", help="agreement between annotators, and with gold given "
                                                                 "the label-audit key")
    p.add_argument("--labels", nargs="+", required=True)
    p.add_argument("--key")
    for p in reports.values():
        p.add_argument("--out", help="also write the JSON report here")
    p = sub.add_parser("error-sample", help="packet of wrong probes for the manual error analysis")
    p.add_argument("run")
    p.add_argument("--arm", choices=ARMS, required=True)
    p.add_argument("--n", type=int, default=40)
    p.add_argument("--out", required=True, help="directory for the packet and the labels template")
    p = sub.add_parser("label-sample", help="blind packet of events for the label audit")
    p.add_argument("data", nargs="+")
    p.add_argument("--per-category", type=int, default=5)
    p.add_argument("--out", required=True, help="directory for the packet, the key and the labels template")
    for p in sub.choices.values():
        p.add_argument("--bootstrap", type=int, default=2000)
        p.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    if args.command == "report":
        conditions = {name: [load_run(r) for r in getattr(args, name)] for name in CONDITIONS}
        _write(report(conditions, args.bootstrap, args.seed), args.out)
    elif args.command == "paired":
        a_runs, b_runs = [load_run(r) for r in args.a], [load_run(r) for r in args.b]
        info = probe_info(a_runs[0]["episodes"])
        if probe_info(b_runs[0]["episodes"]) != info:
            raise SystemExit("the two sides cover different probes")
        _write(paired(correctness(a_runs, args.arm_a), correctness(b_runs, args.arm_b), info,
                      bootstrap=args.bootstrap, seed=args.seed), args.out)
    elif args.command == "memory-classes":
        _write(memory_classes([load_run(r) for r in args.runs], args.bootstrap, args.seed), args.out)
    elif args.command == "structure":
        _write(structure([load_run(r) for r in args.runs]), args.out)
    elif args.command == "agreement":
        _write(agreement_report(args.labels, args.key), args.out)
    elif args.command == "error-sample":
        sample = error_sample(load_run(args.run), args.arm, args.n, args.seed)
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"packet_{args.arm}.md").write_text(error_packet_markdown(sample), encoding="utf-8")
        (out / f"sample_{args.arm}.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1) + "\n",
                                                     encoding="utf-8")
        (out / f"labels_{args.arm}.json").write_text(json.dumps(label_template(
            [i["id"] for i in sample["items"]], "source", ERROR_SOURCES), indent=1) + "\n", encoding="utf-8")
        print(f"{sample['sampled']} of {sample['wrong_probes']} wrong {args.arm} probes -> {out}")
    elif args.command == "label-sample":
        items, key = label_sample(args.data, args.per_category, args.seed)
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "packet.md").write_text(label_packet_markdown(items), encoding="utf-8")
        (out / "key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")
        (out / "labels_template.json").write_text(json.dumps(label_template(
            [i["id"] for i in items], "category", CATEGORIES), indent=1) + "\n", encoding="utf-8")
        print(f"{len(items)} events -> {out}")


if __name__ == "__main__":
    main()
