#!/usr/bin/env python3
"""Fail-closed, standard-library validation of the released v1.1 corpus.

Run from any directory. All rebuild writes are isolated in a temporary directory
inside this package and removed afterward. No source files outside this package
are modified. Structural checks supplement, rather than replace, replay_gold.
"""
import argparse
import collections
import copy
import datetime as dt
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
from scope_memory import protocol  # noqa: E402

SPLITS = ("train", "dev", "test")
MIN_EPISODES = {"train": 600, "dev": 120, "test": 200}
EPISODE_KEYS = {"episode_id", "split", "family", "contrast_group", "attributes", "initial_state", "events", "probes"}
EVENT_KEYS = {"event_id", "date", "dialogue", "gold"}
GOLD_KEYS = {"category", "decision", "state_after", "evidence_message", "rationale"}
PROBE_KEYS = {"probe_id", "after_event", "attribute", "question", "date", "situation_scope_keys", "options", "gold", "category", "probe_type"}
SCHEMA_KEYS = EPISODE_KEYS | EVENT_KEYS | GOLD_KEYS | PROBE_KEYS | {
    "value_aliases", "scopes", "scope", "aliases", "general", "exceptions", "value", "validity", "kind", "from", "to", "role", "content", "scope_key", "scope_keys", "memory_id", "target_id", "evidence_ids", "relations", "operation", "actions", "operations", "status"}
# Bare ordinary English words (date, family, general, window, open, etc.) are
# not machine labels in context. All field names are rejected in key syntax;
# unambiguous machine labels are also rejected as standalone lexical tokens.
BARE_METADATA = {x for x in SCHEMA_KEYS if "_" in x} | {
    "gold", "category", "role", "dialogue", "resolved", "clarify", "user", "assistant"} | set(protocol.CATEGORIES)
META_RE = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(re.escape(x) for x in sorted(BARE_METADATA, key=len, reverse=True)) + r")(?![A-Za-z0-9_])", re.I)
KEY_RE = re.compile(r"[\"'](?:" + "|".join(re.escape(x) for x in sorted(SCHEMA_KEYS, key=len, reverse=True)) + r")[\"']\s*:", re.I)
ISO_IN_DIALOGUE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
PROHIBITED_RULES = ("i won't guess", "i won’t guess", "everything else stays as it was", "this is an exception", "treat this as the default")
CHAIN_NAMES = ("add_then_revise", "add_then_general_preservation")


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def normalized_words(value):
    """Audit token normalization, independently implemented for gate checks."""
    value = unicodedata.normalize("NFKC", value).replace("’", "'").replace("‘", "'").casefold()
    return tuple(re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)*", value))


def text(value, where):
    need(isinstance(value, str) and value.strip() == value and bool(value), f"{where}: nonempty trimmed string required")
    return value


def exact(obj, required, where, optional=()):
    need(isinstance(obj, dict), f"{where}: object required")
    need(required <= set(obj) <= required | set(optional), f"{where}: keys differ (missing={sorted(required - set(obj))}, extra={sorted(set(obj) - required - set(optional))})")


def array(obj, where):
    need(isinstance(obj, list), f"{where}: array required")
    return obj


def unique_strings(values, where, min_length=0):
    array(values, where)
    need(len(values) >= min_length, f"{where}: at least {min_length} entries required")
    normalized = [norm(text(x, where)) for x in values]
    need(len(set(normalized)) == len(values), f"{where}: duplicate values")


def date(value, where):
    text(value, where)
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError as exc:
        raise Invalid(f"{where}: invalid calendar date {value!r}") from exc
    need(parsed.isoformat() == value, f"{where}: ISO YYYY-MM-DD required")
    return parsed


def validity(value, where):
    need(isinstance(value, dict) and value.get("kind") in protocol.VALIDITY_KINDS, f"{where}: invalid validity kind")
    exact(value, {"kind", "from", "to"} if value["kind"] == "window" else {"kind"}, where)
    if value["kind"] == "window":
        need(date(value["from"], where) <= date(value["to"], where), f"{where}: reversed window")


def catalog(item, where):
    exact(item, {"attribute", "options", "scopes"}, where, {"value_aliases"})
    text(item["attribute"], where)
    need(" when " not in f" {norm(item['attribute'])} ", f"{where}: ambiguous canonical CRUD attribute")
    unique_strings(item["options"], where + ".options", 2)
    aliases = item.get("value_aliases", {})
    need(isinstance(aliases, dict) and set(aliases) <= set(item["options"]), f"{where}: aliases for unknown values")
    seen_values = {norm(o): o for o in item["options"]}
    for value, entries in aliases.items():
        unique_strings(entries, where + ".value_aliases")
        for alias in entries:
            n = norm(alias)
            need(n not in seen_values or seen_values[n] == value, f"{where}: ambiguous value alias {alias!r}")
            seen_values[n] = value
    need(isinstance(item["scopes"], dict) and item["scopes"], f"{where}: nonempty scopes object required")
    seen_scopes = {}
    for key, entry in item["scopes"].items():
        text(key, where + ".scope_key")
        exact(entry, {"scope"}, where + ".scope", {"aliases"})
        text(entry["scope"], where + ".scope")
        need(norm(entry["scope"]) != "general", f"{where}: reserved general scope")
        unique_strings(entry.get("aliases", []), where + ".scope.aliases")
        for phrase in [entry["scope"]] + entry.get("aliases", []):
            n = norm(phrase)
            need(n not in seen_scopes or seen_scopes[n] == key, f"{where}: ambiguous scope alias")
            seen_scopes[n] = key


def state(value, catalogs, where):
    exact(value, set(catalogs), where)
    for attribute, entry in value.items():
        exact(entry, {"general", "exceptions"}, where + "." + attribute)
        need(entry["general"] in catalogs[attribute]["options"], f"{where}: unknown general value")
        need(isinstance(entry["exceptions"], dict), f"{where}: exceptions object required")
        for key, exc in entry["exceptions"].items():
            need(key in catalogs[attribute]["scopes"], f"{where}: unknown scope key {key!r}")
            exact(exc, {"value", "validity"}, where + ".exception")
            need(exc["value"] in catalogs[attribute]["options"], f"{where}: unknown exception value")
            validity(exc["validity"], where + ".validity")


def schema_episode(ep, split):
    exact(ep, EPISODE_KEYS, "episode")
    text(ep["episode_id"], "episode_id")
    need(ep["split"] == split, "episode split differs from file")
    text(ep["family"], "family")
    if ep["contrast_group"] is not None:
        text(ep["contrast_group"], "contrast_group")
    array(ep["attributes"], "attributes")
    need(1 <= len(ep["attributes"]) <= 2, "one or two attributes required")
    for item in ep["attributes"]:
        catalog(item, "catalog")
    unique_strings([item["attribute"] for item in ep["attributes"]], "attribute names", 1)
    catalogs = {item["attribute"]: item for item in ep["attributes"]}
    need(len(catalogs) == len(ep["attributes"]), "duplicate attributes")
    state(ep["initial_state"], catalogs, "initial_state")
    array(ep["events"], "events")
    need(4 <= len(ep["events"]) <= 8, "4-8 events required")
    prior_date = None
    ids = set()
    for event in ep["events"]:
        exact(event, EVENT_KEYS, "event")
        eid = text(event["event_id"], "event_id")
        need(eid not in ids and eid != "seed", "duplicate/reserved event ID")
        ids.add(eid)
        current_date = date(event["date"], eid)
        need(prior_date is None or prior_date < current_date, f"{eid}: event dates must strictly increase")
        prior_date = current_date
        dialogue = array(event["dialogue"], eid + ".dialogue")
        need(2 <= len(dialogue) <= 8, f"{eid}: 2-8 dialogue messages required")
        for i, message in enumerate(dialogue):
            exact(message, {"role", "content"}, eid + ".message")
            need(message["role"] == ("user" if i % 2 == 0 else "assistant"), f"{eid}: role alternation/user-first violation")
            content = text(message["content"], eid + ".content")
            need(not META_RE.search(content) and not KEY_RE.search(content), f"{eid}: schema/category/role metadata in dialogue: {content!r}")
            need(not ISO_IN_DIALOGUE.search(content), f"{eid}: dialogue date must be natural English")
            need(not any(rule in norm(content) for rule in PROHIBITED_RULES), f"{eid}: prohibited label-giving phrase")
        gold = event["gold"]
        exact(gold, GOLD_KEYS, eid + ".gold")
        need(gold["category"] in protocol.CATEGORIES, f"{eid}: unknown category")
        need(gold["decision"] == ("clarify" if gold["category"] == "clarify" else "resolved"), f"{eid}: inconsistent decision")
        evidence = gold["evidence_message"]
        need(type(evidence) is int and 1 <= evidence <= len(dialogue) and dialogue[evidence - 1]["role"] == "user", f"{eid}: evidence must point to user message")
        text(gold["rationale"], eid + ".rationale")
        state(gold["state_after"], catalogs, eid + ".state_after")
    array(ep["probes"], "probes")
    seen_probes = set()
    for probe in ep["probes"]:
        exact(probe, PROBE_KEYS, "probe")
        pid = text(probe["probe_id"], "probe_id")
        need(pid not in seen_probes, f"{pid}: duplicate probe ID")
        seen_probes.add(pid)
        need(probe["after_event"] in ids, f"{pid}: unknown checkpoint")
        need(probe["attribute"] in catalogs, f"{pid}: unknown attribute")
        cat = catalogs[probe["attribute"]]
        text(probe["question"], pid + ".question")
        date(probe["date"], pid)
        unique_strings(probe["situation_scope_keys"], pid + ".situation_scope_keys")
        need(set(probe["situation_scope_keys"]) <= set(cat["scopes"]), f"{pid}: unknown situation scope")
        unique_strings(probe["options"], pid + ".options", 2)
        need(set(probe["options"]) <= set(cat["options"]) and probe["gold"] in probe["options"], f"{pid}: invalid options/gold")
        need(probe["category"] in protocol.QA_GROUPS, f"{pid}: invalid QA class")
        need(probe["probe_type"] in protocol.PROBE_TYPES, f"{pid}: invalid probe type")
    need(2 <= len({p["after_event"] for p in ep["probes"]}) <= 4, "2-4 distinct probed checkpoints required")
    return catalogs


def window_boundary(exc, probe):
    v = exc["validity"]
    if v["kind"] != "window":
        return False
    d = date(probe["date"], "probe boundary")
    return (date(v["from"], "window") - d).days == 1 or (d - date(v["to"], "window")).days == 1


def semantics(ep, catalogs):
    before = ep["initial_state"]
    by_event = collections.defaultdict(list)
    for p in ep["probes"]:
        by_event[p["after_event"]].append(p)
    added = set()
    revision_chain = False
    preservation_chain = False
    window_count = 0
    kinds = set()
    for entry in before.values():
        for exc in entry["exceptions"].values():
            kinds.add(exc["validity"]["kind"])
    for event in ep["events"]:
        eid, gold = event["event_id"], event["gold"]
        after = gold["state_after"]
        changes = protocol.state_changes(before, after)
        need(protocol.category_matches(gold["category"], changes), f"{eid}: transition does not match category")
        if changes:
            kind, attr, key = changes[0]
            if kind == "add":
                added.add((attr, key))
            if kind == "revise" and (attr, key) in added:
                revision_chain = True
            if kind == "general":
                preserved = set(before[attr]["exceptions"]) & set(after[attr]["exceptions"])
                preservation_chain |= any((attr, k) in added and before[attr]["exceptions"][k] == after[attr]["exceptions"][k] and protocol.covers(after[attr]["exceptions"][k]["validity"], event["date"]) for k in preserved)
            if kind in ("add", "revise"):
                exc = after[attr]["exceptions"][key]
                if exc["validity"]["kind"] == "window":
                    window_count += 1
                    need(any(p["attribute"] == attr and key in p["situation_scope_keys"] and p["probe_type"] == "boundary" and window_boundary(exc, p) for p in by_event[eid]), f"{eid}: created/revised window lacks immediate boundary probe")
        for entry in after.values():
            for exc in entry["exceptions"].values():
                kinds.add(exc["validity"]["kind"])
        for p in by_event[eid]:
            entry = after[p["attribute"]]
            applicable = [key for key, exc in entry["exceptions"].items() if key in p["situation_scope_keys"] and protocol.covers(exc["validity"], p["date"])]
            need(len(applicable) <= 1, f"{p['probe_id']}: multiple exceptions apply")
            expected = entry["exceptions"][applicable[0]]["value"] if applicable else entry["general"]
            need(p["gold"] == expected, f"{p['probe_id']}: gold violates protocol section 8")
            need(p["category"] == protocol.QA_GROUP_OF[gold["category"]], f"{p['probe_id']}: QA broad class differs from checkpoint event")
            if p["probe_type"] == "target" and changes:
                kind, attr, key = changes[0]
                need(p["attribute"] == attr, f"{p['probe_id']}: target uses an unchanged attribute")
                need((not p["situation_scope_keys"]) if key is None else key in p["situation_scope_keys"], f"{p['probe_id']}: target is not the changed situation")
            if p["probe_type"] == "default":
                need(not p["situation_scope_keys"], f"{p['probe_id']}: default probe must describe ordinary situation")
            if p["probe_type"] == "boundary":
                need(any(key in p["situation_scope_keys"] and window_boundary(exc, p) for key, exc in entry["exceptions"].items()), f"{p['probe_id']}: boundary not one day outside known window")
                need(not applicable, f"{p['probe_id']}: another exception applies at boundary")
            if p["probe_type"] == "neighbor":
                need(bool(p["situation_scope_keys"]), f"{p['probe_id']}: neighbor needs situation scope")
                if changes:
                    kind, attr, key = changes[0]
                    need(p["attribute"] == attr and (key is None or key not in p["situation_scope_keys"]), f"{p['probe_id']}: neighbor is not another scope of changed attribute")
        before = after
    for attr, entry in ep["initial_state"].items():
        for key, exc in entry["exceptions"].items():
            if exc["validity"]["kind"] == "window":
                need(any(p["attribute"] == attr and key in p["situation_scope_keys"] and p["probe_type"] == "boundary" and window_boundary(exc, p) and next(e for e in ep["events"] if e["event_id"] == p["after_event"])["gold"]["state_after"][attr]["exceptions"].get(key) == exc for p in ep["probes"]), "initial window has no boundary probe while present")
    # v1.1 deliberately varies which categories occur in each episode. These
    # chains must be represented in every split, not forced into every story.
    return window_count, kinds, {
        "add_then_revise": revision_chain,
        "add_then_general_preservation": preservation_chain,
    }


def contrast_pair(pair, group):
    need(len(pair) == 2, f"contrast {group}: exactly two episodes required")
    a, b = pair
    need(a["split"] == b["split"], f"contrast {group}: split leakage")
    need(a["family"] == b["family"] and a["attributes"] == b["attributes"] and a["initial_state"] == b["initial_state"], f"contrast {group}: catalogs/family/initial state differ")
    need(len(a["events"]) == len(b["events"]), f"contrast {group}: unequal event counts")
    differences = []
    for event_i, (x, y) in enumerate(zip(a["events"], b["events"])):
        need(x["date"] == y["date"] and len(x["dialogue"]) == len(y["dialogue"]), f"contrast {group}: changed date or message count")
        for message_i, (m, n) in enumerate(zip(x["dialogue"], y["dialogue"])):
            need(m["role"] == n["role"], f"contrast {group}: changed role")
            if m["content"] != n["content"]:
                differences.append((event_i, message_i))
    need(len(differences) == 1, f"contrast {group}: expected exactly one differing message; got {len(differences)}")
    ei, mi = differences[0]
    event_a, event_b = a["events"][ei], b["events"][ei]
    need(event_a["dialogue"][mi]["role"] == "user", f"contrast {group}: differing message is not user")
    need(any(m["role"] == "user" for m in event_a["dialogue"][mi + 1:]), f"contrast {group}: changed message must precede a later identical user message")
    for x, y in zip(a["events"][:ei], b["events"][:ei]):
        need(x["gold"] == y["gold"], f"contrast {group}: gold differs before evidence")
    fields = ("state_after", "decision", "category")
    need(any(event_a["gold"][k] != event_b["gold"][k] for k in fields), f"contrast {group}: gold is not discriminative")
    need(event_a["gold"]["state_after"] != event_b["gold"]["state_after"] or event_a["gold"]["decision"] != event_b["gold"]["decision"], f"contrast {group}: labels differ without substantive decision/state difference")
    return len(event_a["dialogue"]) - mi - 1


def duplicate_safe(pairs):
    obj = {}
    for k, v in pairs:
        need(k not in obj, f"duplicate JSON key {k!r}")
        obj[k] = v
    return obj


def json_load(raw):
    return json.loads(raw, object_pairs_hook=duplicate_safe, parse_constant=lambda x: (_ for _ in ()).throw(Invalid(f"nonfinite JSON constant {x}")))


def read_json(path):
    return json_load(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module_from(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def data_sets(episodes):
    result = {name: set() for name in ("attributes", "scopes", "values", "families", "family_stems")}
    for ep in episodes:
        result["families"].add(norm(ep["family"]))
        result["family_stems"].add(re.sub(r"^(?:train|dev|test)[-_: ]+", "", norm(ep["family"])))
        for c in ep["attributes"]:
            result["attributes"].add(norm(c["attribute"]))
            result["values"].update(norm(v) for v in c["options"])
            result["values"].update(norm(v) for aliases in c.get("value_aliases", {}).values() for v in aliases)
            result["scopes"].update(norm(v) for s in c["scopes"].values() for v in [s["scope"]] + s.get("aliases", []))
    return result


def disjoint(sets, label):
    for a, b in itertools.combinations(SPLITS, 2):
        for field in sets[a]:
            common = sets[a][field] & sets[b][field]
            need(not common, f"{label}: {a}/{b} overlap in {field}: {sorted(common)[:10]}")


def surface_template_sets():
    """Inspect all split-keyed wording banks in the actual dialogue renderer.

    Import the local standard-library-only module with bytecode writes disabled;
    do not call its renderer, alias loader, or any generation/output function.
    Discover dictionaries rather than maintaining an exhaustive allowlist, so
    newly added split-keyed constants cannot silently evade the overlap check.
    """
    surface = module_from(HERE / "surface.py", "scope_v11_surface_validation")
    constants = {name: value for name, value in vars(surface).items()
                 if isinstance(value, dict) and set(value) == set(SPLITS)}
    required = {"REASON_PROMPTS", "OPENERS", "INVITATIONS", "DIRECTIVES", "PERSISTENT",
                "OPEN_DURATION", "WINDOW_DURATION", "ORDINARY", "RETIRES", "UNCERTAIN",
                "ONE_OFF", "FRAMES", "FOLLOWUPS"}
    need(required <= set(constants), "surface.py: missing expected split-keyed wording banks: " +
         ", ".join(sorted(required - set(constants))))

    def strings(value):
        if isinstance(value, str):
            yield norm(value)
        elif isinstance(value, (list, tuple)):
            for item in value:
                yield from strings(item)
        elif isinstance(value, dict):
            for item in value.values():
                yield from strings(item)

    result = {split: set() for split in SPLITS}
    counts = {split: {} for split in SPLITS}
    for name, constant in sorted(constants.items()):
        for split in SPLITS:
            phrases = set(strings(constant[split]))
            if name in required:
                need(phrases and all(phrases), f"surface.py/{name}/{split}: empty wording bank or phrase")
            counts[split][name] = len(phrases)
            result[split].update(phrases)
    need(all(result.values()), "surface.py: split wording coverage must be positive")
    return result, counts


def bank_sets():
    """Bank schema is checked in addition to actual emitted catalog vocabulary."""
    result = {}
    surface_templates, _ = surface_template_sets()
    for split in SPLITS:
        scenarios = read_json(HERE / "banks" / split / "scenarios.json")
        phrases = read_json(HERE / "banks" / split / "phrasing.json")
        alias_bank = read_json(HERE / "banks" / split / "aliases.json")
        need(isinstance(alias_bank, dict) and alias_bank, f"{split}: nonempty alias bank required")
        # Hand-authored bank schema is finalized with build.py; no inferred
        # metadata prefixes are treated as evidence of disjointness.
        scenario_rows = scenarios if isinstance(scenarios, list) else scenarios.get("scenarios", [])
        need(isinstance(scenario_rows, list) and scenario_rows, f"{split}: no scenario bank rows")
        catalogs = []
        families = set()
        attribute_aliases = set()
        for row in scenario_rows:
            need(isinstance(row, dict), f"{split}: bad scenario row")
            if "attributes" in row:
                attrs = copy.deepcopy(row["attributes"])
            else:
                attrs = [{k: v for k, v in row.items() if k in {"attribute", "options", "value_aliases", "scopes"}}]
                if isinstance(attrs[0].get("scopes"), list):
                    unique_strings(attrs[0]["scopes"], split + " bank scopes", 1)
                    attrs[0]["scopes"] = {str(i): {"scope": phrase, "aliases": []}
                                          for i, phrase in enumerate(attrs[0]["scopes"])}
            for c in attrs:
                attribute = c.get("attribute")
                need(attribute in alias_bank, f"{split}: missing alias bank entry for {attribute!r}")
                alias = alias_bank[attribute]
                exact(alias, {"attr_short", "scopes", "options"}, split + " bank aliases", {"topics", "reasons"})
                for field in ("topics", "reasons"):
                    if field in alias:
                        unique_strings(alias[field], split + " bank grounding " + field, 1)
                attribute_aliases.add(norm(text(alias["attr_short"], split + " short attribute phrase")))
                unique_strings(alias["options"], split + " bank value aliases")
                unique_strings(alias["scopes"], split + " bank scope aliases")
                need(len(alias["options"]) == len(c["options"]), f"{split}: value aliases must align with options")
                need(len(alias["scopes"]) == len(c["scopes"]), f"{split}: scope aliases must align with scopes")
                c["value_aliases"] = {value: [natural] for value, natural in zip(c["options"], alias["options"])}
                for entry, natural in zip(c["scopes"].values(), alias["scopes"]):
                    entry["aliases"] = [natural]
                catalog(c, split + " bank catalog")
            catalogs.extend(attrs)
            families.add(norm(text(row.get("family"), split + " bank family")))
        emitted = data_sets([{"family": family, "attributes": catalogs} for family in families])
        need(set(alias_bank) == {c["attribute"] for c in catalogs}, f"{split}: extra or missing attribute in alias bank")
        emitted["attribute_aliases"] = attribute_aliases
        templates = {norm(row[key]) for row in scenario_rows for key in ("opener", "distraction") if key in row}
        templates.update(norm(value) for row in alias_bank.values() for field in ("topics", "reasons") for value in row.get(field, []))
        templates.update(surface_templates[split])
        def leaves(obj):
            if isinstance(obj, str):
                # IDs and metadata are excluded by visiting the template
                # content entries, not by prepending split names.
                templates.add(norm(obj))
            elif isinstance(obj, (list, tuple)):
                for item in obj:
                    leaves(item)
            elif isinstance(obj, dict):
                for key, item in obj.items():
                    if key not in {"split", "version", "schema_version", "id", "template_id", "description", "role"}:
                        leaves(item)
        leaves(phrases)
        need(templates, f"{split}: empty phrase bank")
        emitted["templates"] = templates
        emitted["surface_templates"] = surface_templates[split]
        result[split] = emitted
    return result


def alias_equivalence(corpus):
    """Check aliases using the unchanged protocol's actual canonical readers.

    Exact lexical equivalence is checkable; the naturalness and conversational
    entailment of an alias still need human review.
    """
    results = {}
    for split in SPLITS:
        catalogs = {}
        for ep in corpus[split]:
            for c in ep["attributes"]:
                attribute = c["attribute"]
                if attribute in catalogs:
                    need(catalogs[attribute] == c, f"{split}: inconsistent catalog for {attribute!r}")
                catalogs[attribute] = c
        value_n = scope_n = 0
        for attribute, c in catalogs.items():
            for value in c["options"]:
                aliases = c.get("value_aliases", {}).get(value, [])
                need(aliases, f"{split}/{attribute}: value {value!r} has no natural alias")
                for alias in aliases:
                    need(norm(alias) != norm(value), f"{split}/{attribute}: alias merely repeats canonical value")
                    need(protocol.canonical_value(c, alias) == value, f"{split}/{attribute}: value alias does not canonicalize")
                    value_n += 1
            for key, entry in c["scopes"].items():
                need(entry.get("aliases"), f"{split}/{attribute}: scope {key!r} has no natural alias")
                for alias in entry["aliases"]:
                    need(norm(alias) != norm(entry["scope"]), f"{split}/{attribute}: alias merely repeats canonical scope")
                    need(protocol.scope_key(c, alias) == key, f"{split}/{attribute}: scope alias does not canonicalize")
                    scope_n += 1
        # Seed an actual episode state, render both memory representations with
        # alias values/scopes, then require arm-neutral canonical equality.
        ep = next((e for e in corpus[split] if any(s["exceptions"] for s in e["initial_state"].values())), None)
        need(ep is not None, f"{split}: no initial exception for alias reader test")
        cats = {c["attribute"]: c for c in ep["attributes"]}
        source = ep["initial_state"]
        scope_memory = protocol.ScopeMemory()
        scope_memory.seed(source, cats)
        scope_view = scope_memory.view()
        for record in scope_view:
            c = cats[record["attribute"]]
            record["value"] = c["value_aliases"][record["value"]][0]
            if record["scope"] != protocol.GENERAL:
                key = protocol.scope_key(c, record["scope"])
                record["scope"] = c["scopes"][key]["aliases"][0]
        crud_view = []
        for record in scope_view:
            crud_view.append({"id": record["memory_id"], "text": protocol.crud_sentence(
                record["attribute"], None if record["scope"] == protocol.GENERAL else record["scope"],
                record["value"], record["validity"])})
        expected = protocol.canonical_state(source, cats)
        for arm, view in (("scope", scope_view), ("crud", crud_view)):
            parsed, unmatched = protocol.READERS[arm](view, cats)
            need(not unmatched and parsed == expected, f"{split}: {arm} alias memory reading differs from canonical state")
        results[split] = {"distinct_catalogs": len(catalogs), "value_aliases_checked": value_n,
                          "scope_aliases_checked": scope_n, "both_readers_tested_episode": ep["episode_id"]}
    return results


def structural_baseline_gate(corpus, audit, mode):
    """Independently fit the fixed ordinal/exception-count majority rule."""
    reported = audit["position_active_exception_majority"]
    need(reported["fit_split"] == "train", "structural classifier must fit train only")
    need(reported["label_order_for_ties"] == list(protocol.CATEGORIES), "structural tie order changed")
    rows = {}
    for split in SPLITS:
        rows[split] = []
        for ep in corpus[split]:
            before = ep["initial_state"]
            for ordinal, event in enumerate(ep["events"], 1):
                count = sum(mode == "stored_records" or protocol.covers(exc["validity"], event["date"])
                            for state_entry in before.values() for exc in state_entry["exceptions"].values())
                rows[split].append(((ordinal, count), event["gold"]["category"]))
                before = event["gold"]["state_after"]
    buckets, totals = collections.defaultdict(collections.Counter), collections.Counter()
    for feature, label in rows["train"]:
        buckets[feature][label] += 1
        totals[label] += 1
    fallback = max(protocol.CATEGORIES, key=lambda category: totals[category])
    predictions = {feature: max(protocol.CATEGORIES, key=lambda category: counts[category])
                   for feature, counts in buckets.items()}
    metrics = {}
    for split in ("dev", "test"):
        correct = sum(predictions.get(feature, fallback) == label for feature, label in rows[split])
        count = len(rows[split])
        need(count > 0, f"{split}: no structural evaluation events")
        metric = {"count": count, "correct": correct, "accuracy": correct / count}
        actual = reported[mode]["evaluation"][split]
        need(all(actual[key] == value for key, value in metric.items()), f"{split}: independent {mode} baseline disagrees with audit")
        metrics[split] = metric
    need(metrics["test"]["accuracy"] <= 0.35,
         f"test {mode} structural accuracy {metrics['test']['accuracy']:.4%} exceeds 35% ({metrics['test']['correct']}/{metrics['test']['count']})")
    return {"features": ["1-based event ordinal", "pre-event exception count across all attributes"],
            "exception_count_mode": mode, "fit_split": "train", "test_accuracy_maximum": 0.35,
            "evaluation": metrics}


def last_user_baseline_gate(corpus, audit):
    """Recompute the unchanged v1 multinomial NB, not a substituted model."""
    model = audit["last_user_bow"]
    need(model["fit_split"] == "train" and model["model"] == "multinomial_naive_bayes", "last-user classifier changed")
    need(model["hyperparameters"] == {"token_alpha": 1, "class_prior_alpha": 1}, "last-user NB smoothing changed")
    need(model["label_order_for_ties"] == list(protocol.CATEGORIES), "last-user NB tie order changed")
    rows = {split: [(next(m["content"] for m in reversed(event["dialogue"]) if m["role"] == "user"), event["gold"]["category"])
                    for ep in corpus[split] for event in ep["events"]] for split in SPLITS}
    classes, tokens = collections.Counter(), {category: collections.Counter() for category in protocol.CATEGORIES}
    vocabulary = set()
    for content, category in rows["train"]:
        normalized = normalized_words(content)
        classes[category] += 1
        tokens[category].update(normalized)
        vocabulary.update(normalized)
    prior = {category: math.log((classes[category] + 1) / (len(rows["train"]) + len(protocol.CATEGORIES)))
             for category in protocol.CATEGORIES}
    denominator = {category: math.log(sum(tokens[category].values()) + max(1, len(vocabulary)))
                   for category in protocol.CATEGORIES}
    metrics = {}
    for split in ("dev", "test"):
        correct = 0
        for content, gold in rows[split]:
            counts = collections.Counter(word for word in normalized_words(content) if word in vocabulary)
            score = {category: prior[category] + sum(count * (math.log(tokens[category][word] + 1) - denominator[category])
                                                    for word, count in sorted(counts.items())) for category in protocol.CATEGORIES}
            correct += max(protocol.CATEGORIES, key=lambda category: score[category]) == gold
        count = len(rows[split])
        need(count > 0, f"{split}: no last-user evaluation events")
        metric = {"count": count, "correct": correct, "accuracy": correct / count}
        need(all(model["evaluation"][split][key] == value for key, value in metric.items()), f"{split}: independent unchanged NB disagrees with audit")
        metrics[split] = metric
    need(metrics["test"]["accuracy"] <= 0.40,
         f"test last-user NB accuracy {metrics['test']['accuracy']:.4%} exceeds 40% ({metrics['test']['correct']}/{metrics['test']['count']})")
    return {"fit_split": "train", "test_accuracy_maximum": 0.40, "evaluation": metrics}


def lexical_diversity_gate(corpus, audit, split, kind):
    assistants, event_count, mentions = set(), 0, 0
    for ep in corpus[split]:
        names = [normalized_words(c["attribute"]) for c in ep["attributes"]]
        for event in ep["events"]:
            event_count += 1
            matched = False
            for message in event["dialogue"]:
                words = normalized_words(message["content"])
                if message["role"] == "assistant":
                    assistants.add(words)
                matched |= any(name and any(words[i:i + len(name)] == name for i in range(len(words) - len(name) + 1)) for name in names)
            mentions += matched
    reported = audit["utterance_diversity"][split]
    if kind == "assistant":
        distinct = len(assistants)
        need(reported["unique_normalized_assistant_utterances"] == distinct, "assistant diversity audit mismatch")
        need(distinct >= 1500, f"train: only {distinct} distinct normalized assistant utterances; need at least 1500")
        return {"unique_normalized_assistant_utterances": distinct, "minimum": 1500,
                "normalization": "Exact tuples of NFKC/casefold words, curly apostrophes normalized, punctuation ignored; no fuzzy matching."}
    fraction = mentions / event_count
    need(reported["full_catalog_attribute_mention_event_fraction"] == fraction and reported["full_catalog_attribute_mention_events"] == mentions,
         f"{split}: full attribute mention audit mismatch")
    need(fraction <= 0.40, f"{split}: full catalog attribute mention event fraction {fraction:.4%} exceeds 40% ({mentions}/{event_count})")
    return {"events": event_count, "events_with_full_attribute": mentions, "fraction": fraction, "maximum": 0.40,
            "definition": "Any episode catalog's full canonical attribute as contiguous normalized words in one message, any dialogue role; count each event once."}


def recurring_phrase_gate(corpus, audit, split):
    phrases = audit["class_exclusive_recurring_phrases"]
    need(phrases["ngram_min_words"] == 1 and phrases["ngram_max_words"] == 8, "recurring phrase scope must be 1-8 words, including singleton markers")
    need(phrases["minimum_event_support_for_recurring"] == 2 and phrases["maximum_event_fraction"] == 0.15,
         "recurring phrase support/coverage thresholds changed")
    checked = phrases["by_split"][split]["all_dialogue"]
    counts = collections.Counter(event["gold"]["category"] for ep in corpus[split] for event in ep["events"])
    failures = []
    maxima = {}
    for category in protocol.CATEGORIES:
        row = checked["by_category"][category]
        need(row["events"] == counts[category], f"{split}/{category}: recurring phrase denominator is not category events")
        need(row["max_event_fraction"] == row["max_event_support"] / counts[category], f"{split}/{category}: recurring phrase fraction differs")
        maxima[category] = row["max_event_fraction"]
        if row["violations_count"] or row["max_event_fraction"] > 0.15:
            failures.append(f"{category}: max {row['max_event_fraction']:.4%}; {row['violations_count']} violating phrases; examples={row['violation_examples'][:3]}")
    need(not failures, f"{split}: recurring class-exclusive phrase coverage exceeds 15%: " + "; ".join(failures))
    return {"max_event_fraction_by_category": maxima, "maximum": 0.15,
            "definition": "Contiguous normalized 1-8 word phrases within individual messages, including single-word markers and all dialogue roles, recurring in >=2 events and absent in all other five categories in this split. Each phrase counts once per event; denominator is all events of its sole category in the same split.",
            "scope_limitations": "No noncontiguous, semantic-equivalence or >8-word exhaustive claim; passing is not proof of shortcut freedom."}


def validate_manifest(data, corpus):
    manifest = read_json(data / "manifest.json")
    exact(manifest, {"seed", "files", "format"}, "manifest")
    need(manifest["seed"] == 0 and type(manifest["seed"]) is int, "release manifest seed must be integer zero")
    need(manifest["format"] == "scope-memory-v1", "unknown manifest format")
    expected = {s + ".jsonl" for s in SPLITS} | {"audit.json", "../samples.md"}
    exact(manifest["files"], expected, "manifest.files")
    for filename, info in manifest["files"].items():
        exact(info, {"sha256", "episodes", "categories"} if filename.endswith(".jsonl") else {"sha256"}, filename)
        need(isinstance(info["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", info["sha256"]), f"{filename}: malformed hash")
        need(sha(data / filename) == info["sha256"], f"{filename}: manifest SHA-256 mismatch")
        if filename.endswith(".jsonl"):
            rows = corpus[filename[:-6]]
            need(type(info["episodes"]) is int and info["episodes"] == len(rows), f"{filename}: manifest episode count mismatch")
            counts = dict(collections.Counter(e["gold"]["category"] for ep in rows for e in ep["events"]))
            need(info["categories"] == counts, f"{filename}: manifest category counts mismatch")
    return manifest


def rebuild_check(data):
    with tempfile.TemporaryDirectory(prefix=".validation-rebuild-", dir=HERE) as temp:
        out = Path(temp) / "data"
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "-B", str(HERE / "build.py"), "--seed", "0", "--output-dir", str(out)], cwd=REPO, env=env, text=True, capture_output=True, encoding="utf-8", timeout=240)
        need(result.returncode == 0, f"deterministic rebuild failed ({result.returncode}): {result.stdout}\n{result.stderr}")
        released = {p.relative_to(data).as_posix() for p in data.rglob("*") if p.is_file()}
        rebuilt = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
        need(released == rebuilt, f"rebuild file set differs: {released ^ rebuilt}")
        different = [relative for relative in sorted(released)
                     if (data / relative).read_bytes() != (out / relative).read_bytes()]
        if (data.parent / "samples.md").read_bytes() != (out.parent / "samples.md").read_bytes():
            different.append("../samples.md")
        need(not different, "rebuild bytes differ: " + ", ".join(different))
        return sorted(released) + ["../samples.md"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=HERE / "data")
    args = parser.parse_args(argv)
    data = args.data_dir.resolve()
    errors, report, corpus = [], {}, {}
    def gate(name, function):
        try:
            result = function()
            report[name] = {"passed": True, "details": result}
            print("PASS " + name)
            return result
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
            report[name] = {"passed": False, "error": str(exc)}
            print("FAIL " + errors[-1])
            return None
    def encoding_check():
        count = 0
        for p in HERE.rglob("*"):
            # Interpreter caches are transient binary files, not delivered
            # text artifacts. Never interpret their bytes as UTF-8/LF text.
            if not p.is_file() or "__pycache__" in p.parts or any(part.startswith(".validation-rebuild-") for part in p.parts):
                continue
            raw = p.read_bytes()
            need(not raw.startswith(b"\xef\xbb\xbf"), f"{p.relative_to(HERE)}: UTF-8 BOM")
            need(b"\r" not in raw, f"{p.relative_to(HERE)}: CR rather than LF")
            decoded = raw.decode("utf-8", errors="strict")
            need(not decoded or raw.endswith(b"\n"), f"{p.relative_to(HERE)}: missing final LF")
            count += 1
        return {"files": count}
    gate("utf8_lf", encoding_check)
    def load():
        for split in SPLITS:
            lines = (data / (split + ".jsonl")).read_text(encoding="utf-8").splitlines()
            need(lines and all(line.strip() for line in lines), f"{split}: empty JSONL line")
            corpus[split] = [json_load(line) for line in lines]
        return {s: len(rows) for s, rows in corpus.items()}
    if gate("json_loading", load) is None:
        print(json.dumps({"passed": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    all_ids, groups, stats = set(), collections.defaultdict(list), {}
    episode_errors = []
    replay_count = 0
    for split in SPLITS:
        counts, qa, probe_types, kinds = collections.Counter(), collections.Counter(), collections.Counter(), set()
        event_lengths, attribute_counts, chain_counts = collections.Counter(), collections.Counter(), collections.Counter()
        omitted_category_episodes = 0
        windows = 0
        for ep in corpus[split]:
            label = ep.get("episode_id", "<missing>") if isinstance(ep, dict) else "<not an object>"
            try:
                catalogs = schema_episode(ep, split)
                for identifier in [ep["episode_id"]] + [e["event_id"] for e in ep["events"]] + [p["probe_id"] for p in ep["probes"]]:
                    need(identifier not in all_ids, f"globally reused ID {identifier!r}")
                    all_ids.add(identifier)
                window_n, local_kinds, local_chains = semantics(ep, catalogs)
                windows += window_n
                kinds.update(local_kinds)
                event_lengths[len(ep["events"])] += 1
                attribute_counts[len(ep["attributes"])] += 1
                chain_counts.update(name for name, present in local_chains.items() if present)
                omitted_category_episodes += set(e["gold"]["category"] for e in ep["events"]) < set(protocol.CATEGORIES)
                counts.update(e["gold"]["category"] for e in ep["events"])
                qa.update(p["category"] for p in ep["probes"])
                probe_types.update(p["probe_type"] for p in ep["probes"])
                if ep["contrast_group"] is not None:
                    groups[ep["contrast_group"]].append(ep)
            except Exception as exc:
                episode_errors.append(f"{label}: {type(exc).__name__}: {exc}")
            # Deliberately attempt the authoritative replay on every episode,
            # even when another independent check has already rejected it.
            try:
                protocol.replay_gold(ep)
                replay_count += 1
            except Exception as exc:
                episode_errors.append(f"{label}: replay_gold: {type(exc).__name__}: {exc}")
        stats[split] = {"episodes": len(corpus[split]), "events": dict(counts), "qa_classes": dict(qa), "probe_types": dict(probe_types), "validity_kinds": sorted(kinds), "created_or_revised_windows": windows,
                        "events_per_episode": dict(sorted(event_lengths.items())),
                        "attributes_per_episode": dict(sorted(attribute_counts.items())),
                        "two_attribute_fraction": attribute_counts[2] / len(corpus[split]) if corpus[split] else 0,
                        "episodes_omitting_one_or_more_categories": omitted_category_episodes,
                        "chain_episode_counts": {name: chain_counts[name] for name in CHAIN_NAMES}}
    def episode_gate():
        need(not episode_errors, "\n".join(episode_errors[:100]) + (f"\n... {len(episode_errors) - 100} more" if len(episode_errors) > 100 else ""))
        return {"episodes_replayed": replay_count, "stats": stats}
    gate("schema_transitions_probes_replay_chains", episode_gate)
    def coverage():
        for split in SPLITS:
            s = stats[split]
            need(s["episodes"] >= MIN_EPISODES[split], f"{split}: fewer than {MIN_EPISODES[split]} episodes")
            need(set(s["events"]) == set(protocol.CATEGORIES), f"{split}: missing event category")
            need(set(s["qa_classes"]) == set(protocol.QA_GROUPS), f"{split}: missing QA broad class")
            need(set(s["probe_types"]) == set(protocol.PROBE_TYPES), f"{split}: missing probe type")
            need(set(s["validity_kinds"]) == set(protocol.VALIDITY_KINDS), f"{split}: missing validity type")
            need(set(s["events_per_episode"]) == set(range(4, 9)), f"{split}: every event length 4, 5, 6, 7 and 8 must be represented")
            need(0.27 <= s["two_attribute_fraction"] <= 0.33, f"{split}: two-attribute episode fraction must be 27-33%, got {s['two_attribute_fraction']:.4%}")
            need(s["episodes_omitting_one_or_more_categories"] > 0, f"{split}: no episode omits a category")
            for chain in CHAIN_NAMES:
                need(s["chain_episode_counts"][chain] > 0, f"{split}: no same-episode {chain} chain")
        need(min(stats["test"]["events"].values()) >= 80, "test: fewer than 80 events in a category")
        need(min(stats["test"]["qa_classes"].values()) >= 60, "test: fewer than 60 probes in a QA broad class")
        return stats
    gate("size_and_coverage", coverage)
    def contrasts():
        pairs = collections.Counter()
        suffix = []
        for group, pair in groups.items():
            suffix.append(contrast_pair(pair, group))
            pairs[pair[0]["split"]] += 1
        need(pairs["train"] > 0, "train has no contrast pairs")
        need(pairs["dev"] >= 60 and pairs["test"] >= 60, "dev/test require at least 60 contrast pairs each")
        return {"pairs": dict(pairs), "minimum_identical_suffix_messages": min(suffix)}
    gate("contrast_pairs", contrasts)
    def isolation():
        sets = {s: data_sets(corpus[s]) for s in SPLITS}
        disjoint(sets, "actual corpus")
        need(len(set.union(*(sets[s]["attributes"] for s in SPLITS))) >= 80, "fewer than 80 actual attributes")
        banks = bank_sets()
        disjoint(banks, "hand-authored banks")
        for s in SPLITS:
            for field in sets[s]:
                need(sets[s][field] <= banks[s][field], f"{s}: emitted {field} not in split-specific bank")
        _, surface_counts = surface_template_sets()
        return {s: {field: len(values) for field, values in sets[s].items()} |
                {"bank_templates": len(banks[s]["templates"]),
                 "surface_templates": len(banks[s]["surface_templates"]),
                 "surface_templates_by_constant": surface_counts[s]} for s in SPLITS}
    gate("actual_and_bank_split_isolation", isolation)
    gate("genuine_alias_canonicalization_and_reader_equivalence", lambda: alias_equivalence(corpus))
    audited = {}
    def audit_check():
        module = module_from(HERE / "audit.py", "scope_v1_audit_validation")
        expected = module.audit(data)
        audited["expected"] = expected
        actual = read_json(data / "audit.json")
        need(actual == expected, "audit.json differs from independent audit recomputation")
        canonical_bytes = (json.dumps(expected, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        need((data / "audit.json").read_bytes() == canonical_bytes, "audit bytes are not the deterministic serialization")
        need(all(expected["keyword_occurrences"]["overall"]["present_in_both_buckets"].values()), "one or more shortcut keywords missing from write or no-write dialogues")
        suffix_results = expected["contrast_suffix"]["by_split"]
        for split in SPLITS:
            need(not suffix_results[split]["invalid_groups"], f"{split}: audit reports invalid contrasts")
            for k, row in suffix_results[split]["by_k"].items():
                if row["tied_pairs"]:
                    need(row["tied_transition"]["accuracy_ceiling"] <= 0.5, f"{split}: suffix k={k} transition ceiling exceeds half")
                    need(row["tied_pairs_with_different_transitions"] == row["tied_pairs"], f"{split}: identical-suffix pair lacks discriminative transition")
        for split in ("dev", "test"):
            model = expected["last_user_bow"]
            need(model["fit_split"] == "train", "last-user classifier must fit train only")
            need(0 <= model["evaluation"][split]["accuracy"] <= 1, f"{split}: invalid lexical classifier accuracy")
        ngram = expected["train_test_longest_common_ngram"]
        n = ngram["length_words"]
        need(type(n) is int and n >= 0, "invalid longest ngram length")
        def words(value):
            value = unicodedata.normalize("NFKC", value).replace("’", "'").replace("‘", "'").casefold()
            return tuple(re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)*", value))
        if n:
            for split in ("train", "test"):
                witness = ngram[split + "_example"]
                ep = next(e for e in corpus[split] if e["episode_id"] == witness["episode_id"])
                ev = next(e for e in ep["events"] if e["event_id"] == witness["event_id"])
                original = ev["dialogue"][witness["message_index"] - 1]["content"]
                need(original == witness["text"], "ngram witness is not actual dialogue")
                tokens = words(original)
                offset = witness["word_start"]
                need(type(offset) is int and offset >= 0, "invalid ngram witness offset")
                need(" ".join(tokens[offset:offset + n]) == ngram["phrase"] and len(tokens[offset:offset + n]) == n, "ngram witness phrase/length mismatch")
        # Independent maximality proof: if no common (n+1)-gram exists within
        # individual turns, no longer common contiguous sequence can exist.
        width = n + 1
        train_tokens = {words(m["content"]) for ep in corpus["train"] for e in ep["events"] for m in e["dialogue"]}
        train_grams = {tokens[i:i + width] for tokens in train_tokens for i in range(len(tokens) - width + 1)}
        test_tokens = {words(m["content"]) for ep in corpus["test"] for e in ep["events"] for m in e["dialogue"]}
        need(not any(tokens[i:i + width] in train_grams for tokens in test_tokens for i in range(len(tokens) - width + 1)), "reported longest ngram is not maximal")
        return {"longest_common_ngram": ngram, "last_user_bow_accuracy": {s: expected["last_user_bow"]["evaluation"][s]["accuracy"] for s in ("dev", "test")}, "all_shortcut_keywords_in_both_buckets": True}
    gate("audit_recomputation_and_shortcuts", audit_check)
    # These fail separately so a structural miss cannot hide a lexical miss.
    # They use independently recomputed audit results, not an unverified file.
    for mode in ("date_active", "stored_records"):
        gate("v11_structural_baseline_" + mode, lambda mode=mode: structural_baseline_gate(corpus, audited["expected"], mode))
    gate("v11_unchanged_last_user_naive_bayes", lambda: last_user_baseline_gate(corpus, audited["expected"]))
    gate("v11_train_assistant_diversity", lambda: lexical_diversity_gate(corpus, audited["expected"], "train", "assistant"))
    for split in SPLITS:
        gate("v11_full_attribute_mentions_" + split, lambda split=split: lexical_diversity_gate(corpus, audited["expected"], split, "attribute"))
        gate("v11_class_exclusive_recurring_phrases_" + split, lambda split=split: recurring_phrase_gate(corpus, audited["expected"], split))
    def longer_phrase_gate(split):
        root = audited["expected"]["class_exclusive_long_phrases"]
        row = root["by_split"][split]
        need(root["ngram_min_words"] == 9 and root["maximum_event_fraction"] == 0.15,
             "longer-phrase search must extend the same 15% gate past eight words")
        need(row["exhaustive_through_max_message_words"] and
             row["events"] == sum(len(ep["events"]) for ep in corpus[split]),
             f"{split}: incomplete longer-phrase threshold audit")
        need(row["all_categories_within_threshold"] and row["violations_count"] == 0,
             f"{split}: {row['violations_count']} >15% class-exclusive phrases of nine or more words")
        return {"maximum_message_words": row["maximum_message_words"],
                "stop_reason": row["stop_reason"], "violations_count": row["violations_count"]}
    for split in SPLITS:
        gate("v11_class_exclusive_long_phrases_" + split, lambda split=split: longer_phrase_gate(split))
    def legacy_check():
        module = module_from(HERE / "build.py", "scope_v1_build_validation")
        result = module.legacy_overlap(corpus)
        need(len(result) >= 4, "not all four old release families covered by signature bank")
        need(all(row["old_examples"] > 0 for row in result.values()), "empty legacy signature source")
        return result
    gate("legacy_exact_exclusion", legacy_check)
    def samples_check():
        sample = (data.parent / "samples.md").read_text(encoding="utf-8")
        sections = re.split(r"^## (Train|Dev|Test)\s*$", sample, flags=re.M)
        need(len(sections) == 7, "samples must have one section per split")
        for i in range(1, len(sections), 2):
            split, body = sections[i].casefold(), sections[i + 1]
            headings = re.findall(r"^### (\S+) .*?$", body, flags=re.M)
            need(len(headings) == 10 and len(set(headings)) == 10, f"{split}: samples needs exactly ten distinct episodes")
            known = {ep["episode_id"]: ep for ep in corpus[split]}
            need(set(headings) <= set(known), f"{split}: sample episode not in split")
            for eid in headings:
                for event in known[eid]["events"]:
                    need(event["event_id"] in body, f"{eid}: sampled event omitted")
                    need(all(m["content"] in body for m in event["dialogue"]), f"{eid}: sampled dialogue omitted")
        return {"episodes_per_split": 10}
    gate("readable_samples", samples_check)
    gate("manifest_integrity", lambda: validate_manifest(data, corpus))
    gate("deterministic_rebuild_bytes", lambda: rebuild_check(data))
    print(json.dumps({"passed": not errors, "failed_gates": len(errors), "checks": report}, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
