"""Memory revision protocol v1 (docs/protocol.md): executors, gold projection and readers.

The scope-aware and CRUD arms see byte-identical event evidence and differ only in
how memory is represented and revised. Gold outputs for both arms are projected
from consecutive arm-neutral gold states by one fixed mapping (protocol section 6).

  python3 -m scope_memory.protocol check training/scope_revision_v1/data/dev.jsonl
  python3 -m scope_memory.protocol export-sft training/scope_revision_v1/data/train.jsonl --out OUT_DIR
"""
import argparse
import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

ARMS = ("scope", "crud")
CATEGORIES = ("general_update", "scoped_exception", "exception_revision", "exception_retirement",
              "stable_preference", "clarify")
QA_GROUPS = ("general_update", "scoped_exception", "exception_revision", "stable_preference")
QA_GROUP_OF = {"general_update": "general_update", "scoped_exception": "scoped_exception",
               "exception_revision": "exception_revision", "exception_retirement": "exception_revision",
               "stable_preference": "stable_preference", "clarify": "stable_preference"}
CHANGE_OF = {"general_update": "general", "scoped_exception": "add", "exception_revision": "revise",
             "exception_retirement": "retire"}
PROBE_TYPES = ("target", "default", "neighbor", "boundary")
DECISIONS = ("resolved", "clarify")
VALIDITY_KINDS = ("persistent", "window", "open")
SCOPE_OPERATIONS = ("ADD", "REVISE", "RETIRE", "NOOP")
CRUD_OPERATIONS = ("ADD", "UPDATE", "DELETE", "NOOP")
GENERAL = "general"
PERSISTENT = {"kind": "persistent"}
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
CRUD_EXCEPTION = re.compile(
    r"For (?P<attribute>.+?) when (?P<scope>.+?), the user prefers (?P<value>.+?)"
    r"(?: from (?P<start>\d{4}-\d{2}-\d{2}) through (?P<end>\d{4}-\d{2}-\d{2})|(?P<open> for now, with no end date given))?\.")
CRUD_GENERAL = re.compile(r"For (?P<attribute>.+?), the user prefers (?P<value>.+)\.")

POLICY_INSTRUCTIONS = {
    "scope": (
        "You maintain a user's long-term preference memory. Read the memory and the new conversation and "
        "return one JSON object {\"decision\": \"resolved\" or \"clarify\", \"actions\": [...]}. Records have "
        "memory_id, attribute, value, scope (\"general\" or a situation), validity, relations and evidence_ids. "
        "Actions: ADD {operation, attribute, value, scope, validity, relations, evidence_ids}; REVISE "
        "{operation, target_id, value, scope, validity, relations, evidence_ids}, which replaces target_id; "
        "RETIRE {operation, target_id, evidence_ids}, which removes a situation-specific record so that "
        "situation follows the general preference again; NOOP {operation}, alone. Validity is "
        "{\"kind\": \"persistent\"}, {\"kind\": \"window\", \"from\": \"YYYY-MM-DD\", \"to\": \"YYYY-MM-DD\"} or "
        "{\"kind\": \"open\"}. A situation-specific record needs relations [{\"type\": \"EXCEPTION_TO\", "
        "\"target\": <id of the general record>}]. evidence_ids name the event that supports the write. "
        "Store only lasting preferences of the user; one-off requests and other people's preferences need "
        "NOOP. If the user has not settled what should change, answer \"clarify\" with a single NOOP."),
    "crud": (
        "You maintain a user's long-term preference memory as free-text records. Read the memory and the new "
        "conversation and return one JSON object {\"decision\": \"resolved\" or \"clarify\", \"operations\": "
        "[...]}. Operations: ADD {op, text}; UPDATE {op, id, text}; DELETE {op, id}; NOOP {op}, alone. You may "
        "keep any number of records, including separate records for situations that differ from the usual "
        "preference, and delete records that no longer apply. Store only lasting preferences of the user; "
        "one-off requests and other people's preferences need NOOP. If the user has not settled what should "
        "change, answer \"clarify\" with a single NOOP."),
}


class Rejected(Exception):
    """An output that violates the protocol; the executor keeps its previous state."""


def norm(text):
    return " ".join(str(text).split()).casefold()


def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def validity_error(validity):
    if not isinstance(validity, dict) or validity.get("kind") not in VALIDITY_KINDS:
        return "bad_validity"
    if validity["kind"] == "window":
        start, end = validity.get("from"), validity.get("to")
        if (set(validity) != {"kind", "from", "to"}
                or not all(isinstance(x, str) and ISO_DATE.fullmatch(x) for x in (start, end)) or start > end):
            return "bad_window"
    elif set(validity) != {"kind"}:
        return "bad_validity"
    return None


def covers(validity, date):
    return validity["kind"] != "window" or validity["from"] <= date <= validity["to"]


def crud_sentence(attribute, scope, value, validity):
    """Fixed CRUD projection of one record (protocol section 6)."""
    if scope is None:
        return f"For {attribute}, the user prefers {value}."
    tail = {"persistent": "", "open": " for now, with no end date given"}.get(validity["kind"])
    if tail is None:
        tail = f" from {validity['from']} through {validity['to']}"
    return f"For {attribute} when {scope}, the user prefers {value}{tail}."


class ScopeMemory:
    """Executor for the scope-aware arm (protocol section 4)."""

    def __init__(self):
        self.records = {}
        self.counter = 0
        self.log = []

    def view(self):
        fields = ("memory_id", "attribute", "value", "scope", "validity", "relations", "evidence_ids")
        return [{k: copy.deepcopy(r[k]) for k in fields} for r in self.records.values() if r["status"] == "active"]

    def general_id(self, attribute):
        return next((r["memory_id"] for r in self.records.values()
                     if r["status"] == "active" and r["attribute"] == attribute and r["scope"] == GENERAL), None)

    def seed(self, state, catalogs):
        """Create the initial records; return {(attribute, scope_key or None): memory_id}."""
        keys = {}
        for attribute, entry in state.items():
            keys[(attribute, None)] = self._create(attribute, entry["general"], GENERAL, PERSISTENT, [], ["seed"])
            for key in sorted(entry["exceptions"]):
                exc = entry["exceptions"][key]
                keys[(attribute, key)] = self._create(
                    attribute, exc["value"], catalogs[attribute]["scopes"][key]["scope"], exc["validity"],
                    [{"type": "EXCEPTION_TO", "target": keys[(attribute, None)]}], ["seed"])
        return keys

    def _create(self, attribute, value, scope, validity, relations, evidence):
        self.counter += 1
        memory_id = f"m{self.counter}"
        self.records[memory_id] = {"memory_id": memory_id, "attribute": attribute, "value": value, "scope": scope,
                                   "validity": dict(validity), "relations": [dict(x) for x in relations],
                                   "evidence_ids": list(evidence), "status": "active"}
        return memory_id

    def apply(self, output, event_id, seen):
        """Apply one output; return (rejection reason or None, ids created per action)."""
        records, counter = copy.deepcopy(self.records), self.counter
        try:
            created = self._apply(output, set(seen))
        except Rejected as exc:
            self.records, self.counter = records, counter
            self.log.append({"event_id": event_id, "accepted": False, "reason": str(exc)})
            return str(exc), []
        self.log.append({"event_id": event_id, "accepted": True, "created": created})
        return None, created

    def _apply(self, output, seen):
        if not isinstance(output, dict) or output.get("decision") not in DECISIONS:
            raise Rejected("bad_decision")
        actions = output.get("actions")
        if not isinstance(actions, list) or not actions or not all(isinstance(a, dict) for a in actions):
            raise Rejected("bad_actions")
        operations = [a.get("operation") for a in actions]
        if any(op not in SCOPE_OPERATIONS for op in operations):
            raise Rejected("unknown_operation")
        if "NOOP" in operations:
            if len(operations) != 1:
                raise Rejected("noop_not_alone")
            return [None]
        if output["decision"] == "clarify":
            raise Rejected("clarify_with_writes")
        targets = [str(a.get("target_id")) for a in actions if a["operation"] != "ADD"]
        if len(targets) != len(set(targets)):
            raise Rejected("target_repeated")
        created = [self._action(a, seen) for a in actions]
        self._check_invariants()
        return created

    def _action(self, action, seen):
        evidence = action.get("evidence_ids")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(e, str) and e in seen for e in evidence):
            raise Rejected("bad_evidence")
        target = None
        if action["operation"] in ("REVISE", "RETIRE"):
            target_id = action.get("target_id")
            target = self.records.get(target_id) if isinstance(target_id, str) else None
            if target is None or target["status"] != "active":
                raise Rejected("unknown_target")
        if action["operation"] == "RETIRE":
            if target["scope"] == GENERAL:
                raise Rejected("retire_general")
            target["status"] = "retired"
            target["retired_by"] = list(evidence)
            return None
        value, scope, validity = action.get("value"), action.get("scope"), action.get("validity")
        relations = action.get("relations", [])
        if not isinstance(value, str) or not value.strip():
            raise Rejected("bad_value")
        if not isinstance(scope, str) or not scope.strip():
            raise Rejected("bad_scope")
        reason = validity_error(validity)
        if reason:
            raise Rejected(reason)
        if not isinstance(relations, list) or not all(
                isinstance(x, dict) and x.get("type") in ("EXCEPTION_TO", "REPLACES") and isinstance(x.get("target"), str)
                for x in relations):
            raise Rejected("bad_relations")
        is_general = norm(scope) == GENERAL
        if action["operation"] == "ADD":
            attribute = action.get("attribute")
            if not isinstance(attribute, str) or not attribute.strip():
                raise Rejected("bad_attribute")
            attribute = " ".join(attribute.split())
            if is_general and self.general_id(attribute):
                raise Rejected("second_general")
        else:
            attribute = target["attribute"]
            if is_general != (target["scope"] == GENERAL):
                raise Rejected("revise_changes_kind")
        edges = [{"type": "EXCEPTION_TO", "target": x["target"]} for x in relations if x["type"] == "EXCEPTION_TO"]
        if is_general and (edges or validity["kind"] != "persistent"):
            raise Rejected("bad_general_record")
        if not is_general and len(edges) != 1:
            raise Rejected("exception_needs_one_edge")
        general = self.records.get(edges[0]["target"]) if edges else None
        if action["operation"] == "ADD" and general is not None and norm(general["attribute"]) == norm(attribute):
            attribute = general["attribute"]
        new_id = self._create(attribute, value.strip(), GENERAL if is_general else " ".join(scope.split()),
                              validity, edges, evidence)
        if target is not None:
            self.records[new_id]["relations"].append({"type": "REPLACES", "target": target["memory_id"]})
            target["status"] = "retired"
            target["retired_by"] = list(evidence)
            if is_general:
                for other in self.records.values():
                    if other["status"] == "active":
                        for edge in other["relations"]:
                            if edge["type"] == "EXCEPTION_TO" and edge["target"] == target["memory_id"]:
                                edge["target"] = new_id
        return new_id

    def _check_invariants(self):
        active = [r for r in self.records.values() if r["status"] == "active"]
        if any(n > 1 for n in Counter(r["attribute"] for r in active if r["scope"] == GENERAL).values()):
            raise Rejected("two_general_records")
        for record in active:
            if record["scope"] == GENERAL:
                continue
            edge = next(x for x in record["relations"] if x["type"] == "EXCEPTION_TO")
            general = self.records.get(edge["target"])
            if (general is None or general["status"] != "active" or general["scope"] != GENERAL
                    or general["attribute"] != record["attribute"]):
                raise Rejected("exception_without_general")


class CrudMemory:
    """Executor for the CRUD arm (protocol section 5): opaque ids and free-text records."""

    def __init__(self):
        self.records = {}
        self.counter = 0
        self.log = []

    def view(self):
        return [{"id": i, "text": t} for i, t in self.records.items()]

    def seed(self, state, catalogs):
        keys = {}
        for attribute, entry in state.items():
            keys[(attribute, None)] = self._create(crud_sentence(attribute, None, entry["general"], PERSISTENT))
            for key in sorted(entry["exceptions"]):
                exc = entry["exceptions"][key]
                keys[(attribute, key)] = self._create(crud_sentence(
                    attribute, catalogs[attribute]["scopes"][key]["scope"], exc["value"], exc["validity"]))
        return keys

    def _create(self, text):
        self.counter += 1
        record_id = f"m{self.counter}"
        self.records[record_id] = text
        return record_id

    def apply(self, output, event_id=None, seen=None):
        """Apply one output; return (rejection reason or None, ids created per operation)."""
        records, counter = dict(self.records), self.counter
        try:
            created = self._apply(output)
        except Rejected as exc:
            self.records, self.counter = records, counter
            self.log.append({"event_id": event_id, "accepted": False, "reason": str(exc)})
            return str(exc), []
        self.log.append({"event_id": event_id, "accepted": True, "created": created})
        return None, created

    def _apply(self, output):
        if not isinstance(output, dict) or output.get("decision") not in DECISIONS:
            raise Rejected("bad_decision")
        operations = output.get("operations")
        if not isinstance(operations, list) or not operations or not all(isinstance(o, dict) for o in operations):
            raise Rejected("bad_operations")
        names = [o.get("op") for o in operations]
        if any(name not in CRUD_OPERATIONS for name in names):
            raise Rejected("unknown_operation")
        if "NOOP" in names:
            if len(names) != 1:
                raise Rejected("noop_not_alone")
            return [None]
        if output["decision"] == "clarify":
            raise Rejected("clarify_with_writes")
        ids = [str(o.get("id")) for o in operations if o["op"] != "ADD"]
        if len(ids) != len(set(ids)):
            raise Rejected("target_repeated")
        created = []
        for o in operations:
            if o["op"] != "ADD" and not (isinstance(o.get("id"), str) and o["id"] in self.records):
                raise Rejected("unknown_target")
            if o["op"] != "DELETE" and not (isinstance(o.get("text"), str) and o["text"].strip()):
                raise Rejected("bad_text")
            if o["op"] == "ADD":
                created.append(self._create(" ".join(o["text"].split())))
            elif o["op"] == "UPDATE":
                self.records[o["id"]] = " ".join(o["text"].split())
                created.append(None)
            else:
                del self.records[o["id"]]
                created.append(None)
        return created


def catalogs_of(episode):
    return {a["attribute"]: a for a in episode["attributes"]}


def _attribute_lookup(catalogs, text):
    return next((name for name in catalogs if norm(name) == norm(text)), None)


def canonical_value(catalog, text):
    """Map a value or one of its aliases to the catalog option; unknown text is returned unchanged."""
    for option in catalog["options"]:
        if norm(text) in {norm(option)} | {norm(a) for a in catalog.get("value_aliases", {}).get(option, [])}:
            return option
    return " ".join(str(text).split())


def scope_key(catalog, phrase):
    for key, entry in catalog["scopes"].items():
        if norm(phrase) in {norm(entry["scope"])} | {norm(a) for a in entry.get("aliases", [])}:
            return key
    return None


def canonical_state(state, catalogs):
    return {attribute: {"general": canonical_value(catalogs[attribute], entry["general"]),
                        "exceptions": {key: {"value": canonical_value(catalogs[attribute], exc["value"]),
                                             "validity": dict(exc["validity"])}
                                       for key, exc in entry["exceptions"].items()}}
            for attribute, entry in state.items()}


def read_scope_state(view, catalogs):
    """Arm-neutral state from scope-aware records; records that do not map to the catalog are listed apart."""
    state, unmatched = {}, []
    for record in view:
        attribute = _attribute_lookup(catalogs, record["attribute"])
        key = None if attribute is None or record["scope"] == GENERAL else scope_key(catalogs[attribute], record["scope"])
        entry = state.setdefault(attribute, {"general": None, "exceptions": {}}) if attribute else None
        if attribute is None or (record["scope"] != GENERAL and (key is None or key in entry["exceptions"])):
            unmatched.append(record["memory_id"])
            continue
        value = canonical_value(catalogs[attribute], record["value"])
        if record["scope"] == GENERAL:
            entry["general"] = value
        else:
            entry["exceptions"][key] = {"value": value, "validity": dict(record["validity"])}
    return state, unmatched


def read_crud_state(view, catalogs):
    """Arm-neutral state from CRUD records written in the canonical sentences; other text is listed apart."""
    state, unmatched = {}, []
    for record in view:
        text = " ".join(record["text"].split())
        match = CRUD_EXCEPTION.fullmatch(text)
        general = match is None
        if general:
            match = CRUD_GENERAL.fullmatch(text)
        attribute = _attribute_lookup(catalogs, match["attribute"]) if match else None
        key = None if attribute is None or general else scope_key(catalogs[attribute], match["scope"])
        entry = state.setdefault(attribute, {"general": None, "exceptions": {}}) if attribute else None
        if attribute is None or (general and entry["general"] is not None) or (
                not general and (key is None or key in entry["exceptions"])):
            unmatched.append(record["id"])
            continue
        value = canonical_value(catalogs[attribute], match["value"])
        if general:
            entry["general"] = value
            continue
        if match["start"]:
            validity = {"kind": "window", "from": match["start"], "to": match["end"]}
        else:
            validity = {"kind": "open"} if match["open"] else dict(PERSISTENT)
        entry["exceptions"][key] = {"value": value, "validity": validity}
    return state, unmatched


READERS = {"scope": read_scope_state, "crud": read_crud_state}


def oracle_answer(state, probe):
    """Value for a probe from an arm-neutral state; None when the state has no answer or two exceptions apply."""
    entry = state.get(probe["attribute"])
    if entry is None:
        return None
    hits = [exc["value"] for key, exc in entry["exceptions"].items()
            if key in probe["situation_scope_keys"] and covers(exc["validity"], probe["date"])]
    if len(hits) > 1:
        return None
    return hits[0] if hits else entry["general"]


def state_changes(before, after):
    """List (kind, attribute, scope_key) changes; exception changes come before general ones."""
    if set(before) != set(after):
        raise ValueError("attributes differ between states")
    exceptions, generals = [], []
    for attribute in after:
        old, new = before[attribute], after[attribute]
        if old["general"] != new["general"]:
            generals.append(("general", attribute, None))
        for key in sorted(set(old["exceptions"]) | set(new["exceptions"])):
            if key not in new["exceptions"]:
                exceptions.append(("retire", attribute, key))
            elif key not in old["exceptions"]:
                exceptions.append(("add", attribute, key))
            elif old["exceptions"][key] != new["exceptions"][key]:
                exceptions.append(("revise", attribute, key))
    return exceptions + generals


def category_matches(category, changes):
    if category in ("stable_preference", "clarify"):
        return not changes
    return len(changes) == 1 and changes[0][0] == CHANGE_OF.get(category)


def gold_scope_output(changes, gold, catalogs, keys, event_id):
    if not changes:
        return {"decision": gold["decision"], "actions": [{"operation": "NOOP"}]}
    after = gold["state_after"]
    actions = []
    for kind, attribute, key in changes:
        general_id = keys[(attribute, None)]
        if kind == "general":
            actions.append({"operation": "REVISE", "target_id": general_id, "value": after[attribute]["general"],
                            "scope": GENERAL, "validity": dict(PERSISTENT), "relations": [],
                            "evidence_ids": [event_id]})
        elif kind == "retire":
            actions.append({"operation": "RETIRE", "target_id": keys[(attribute, key)], "evidence_ids": [event_id]})
        else:
            exc = after[attribute]["exceptions"][key]
            head = ({"operation": "ADD", "attribute": attribute} if kind == "add"
                    else {"operation": "REVISE", "target_id": keys[(attribute, key)]})
            actions.append({**head, "value": exc["value"], "scope": catalogs[attribute]["scopes"][key]["scope"],
                            "validity": dict(exc["validity"]),
                            "relations": [{"type": "EXCEPTION_TO", "target": general_id}],
                            "evidence_ids": [event_id]})
    return {"decision": gold["decision"], "actions": actions}


def gold_crud_output(changes, gold, catalogs, keys):
    if not changes:
        return {"decision": gold["decision"], "operations": [{"op": "NOOP"}]}
    after = gold["state_after"]
    operations = []
    for kind, attribute, key in changes:
        if kind == "general":
            operations.append({"op": "UPDATE", "id": keys[(attribute, None)],
                               "text": crud_sentence(attribute, None, after[attribute]["general"], PERSISTENT)})
        elif kind == "retire":
            operations.append({"op": "DELETE", "id": keys[(attribute, key)]})
        else:
            exc = after[attribute]["exceptions"][key]
            text = crud_sentence(attribute, catalogs[attribute]["scopes"][key]["scope"], exc["value"], exc["validity"])
            operations.append({"op": "ADD", "text": text} if kind == "add"
                              else {"op": "UPDATE", "id": keys[(attribute, key)], "text": text})
    return {"decision": gold["decision"], "operations": operations}


def _update_keys(keys, changes, created):
    for (kind, attribute, key), new_id in zip(changes, created):
        slot = (attribute, None) if kind == "general" else (attribute, key)
        if kind == "retire":
            keys.pop(slot, None)
        elif new_id is not None:
            keys[slot] = new_id


def policy_input(view, event):
    """What the policy sees: its own memory view plus the event; the event part is identical across arms."""
    return {"memory": view, "event": {"event_id": event["event_id"], "date": event["date"],
                                      "dialogue": event["dialogue"]}}


def gold_trajectory(episode):
    """Yield one step per event along the gold path, with both arms' memories before the event and gold outputs."""
    catalogs = catalogs_of(episode)
    memories = {"scope": ScopeMemory(), "crud": CrudMemory()}
    state = episode["initial_state"]
    keys = {arm: memories[arm].seed(state, catalogs) for arm in ARMS}
    seen = ["seed"]
    for event in episode["events"]:
        gold = event["gold"]
        changes = state_changes(state, gold["state_after"])
        before = {arm: copy.deepcopy(memories[arm]) for arm in ARMS}
        seen.append(event["event_id"])
        outputs = {"scope": gold_scope_output(changes, gold, catalogs, keys["scope"], event["event_id"]),
                   "crud": gold_crud_output(changes, gold, catalogs, keys["crud"])}
        rejections = {}
        for arm in ARMS:
            rejections[arm], created = memories[arm].apply(outputs[arm], event["event_id"], seen)
            _update_keys(keys[arm], changes, created)
        yield {"event": event, "changes": changes, "state_before": state, "before": before, "outputs": outputs,
               "rejections": rejections, "after_views": {arm: memories[arm].view() for arm in ARMS},
               "seen": list(seen)}
        state = gold["state_after"]


def _state_problems(state, catalogs, where):
    problems = []
    if not isinstance(state, dict) or set(state) != set(catalogs):
        return [f"{where}: attributes must match the catalog"]
    for attribute, entry in state.items():
        catalog = catalogs[attribute]
        if not isinstance(entry, dict) or entry.get("general") not in catalog["options"]:
            problems.append(f"{where}: {attribute} general value must be an option")
            continue
        for key, exc in entry.get("exceptions", {}).items():
            if key not in catalog["scopes"]:
                problems.append(f"{where}: unknown scope key {key!r}")
            elif exc.get("value") not in catalog["options"] or validity_error(exc.get("validity")):
                problems.append(f"{where}: bad exception {key!r}")
    return problems


def check_structure(episode):
    """Static checks of protocol section 1 (formats, ids, dates, roles, catalogs)."""
    problems = []
    for field in ("episode_id", "attributes", "initial_state", "events"):
        if field not in episode:
            return [f"missing {field}"]
    catalogs = catalogs_of(episode)
    if len(catalogs) != len(episode["attributes"]) or not 1 <= len(catalogs) <= 2:
        problems.append("one or two uniquely named attributes required")
    for name, catalog in catalogs.items():
        options = catalog.get("options", [])
        if " when " in f" {name} " or not options or len({norm(o) for o in options}) != len(options):
            problems.append(f"catalog {name!r}: bad name or options")
        if any(o not in options for o in catalog.get("value_aliases", {})):
            problems.append(f"catalog {name!r}: aliases for unknown options")
        if not isinstance(catalog.get("scopes"), dict) or any(not s.get("scope") for s in catalog["scopes"].values()):
            problems.append(f"catalog {name!r}: bad scopes")
    if problems:
        return problems
    problems += _state_problems(episode["initial_state"], catalogs, "initial_state")
    event_ids, last_date = set(), ""
    if not 4 <= len(episode["events"]) <= 8:
        problems.append("4-8 events required")
    for event in episode["events"]:
        eid = event.get("event_id")
        if eid in event_ids or eid == "seed" or not isinstance(eid, str):
            problems.append(f"bad or repeated event id {eid!r}")
        event_ids.add(eid)
        date = event.get("date", "")
        if not (isinstance(date, str) and ISO_DATE.fullmatch(date)) or date <= last_date:
            problems.append(f"{eid}: dates must be ISO and strictly increasing")
        last_date = date if isinstance(date, str) else last_date
        dialogue = event.get("dialogue", [])
        if not isinstance(dialogue, list) or not all(isinstance(m, dict) for m in dialogue):
            dialogue = []
        if (not 2 <= len(dialogue) <= 8 or any(not isinstance(m.get("content"), str) or not m["content"].strip()
                                                for m in dialogue)
                or any(m.get("role") != ("user" if i % 2 == 0 else "assistant") for i, m in enumerate(dialogue))):
            problems.append(f"{eid}: dialogue needs 2-8 non-empty messages alternating from the user")
        gold = event.get("gold", {})
        if gold.get("category") not in CATEGORIES or gold.get("decision") not in DECISIONS:
            problems.append(f"{eid}: bad category or decision")
        index = gold.get("evidence_message")
        if not (isinstance(index, int) and 1 <= index <= len(dialogue) and dialogue[index - 1].get("role") == "user"):
            problems.append(f"{eid}: evidence_message must point to a user message")
        problems += _state_problems(gold.get("state_after"), catalogs, eid)
    probe_ids = set()
    for probe in episode.get("probes", []):
        pid = probe.get("probe_id")
        catalog = catalogs.get(probe.get("attribute"))
        if pid in probe_ids or probe.get("after_event") not in event_ids or catalog is None:
            problems.append(f"probe {pid!r}: bad id, event or attribute")
            continue
        probe_ids.add(pid)
        if (not ISO_DATE.fullmatch(str(probe.get("date"))) or probe.get("category") not in QA_GROUPS
                or probe.get("probe_type") not in PROBE_TYPES
                or any(k not in catalog["scopes"] for k in probe.get("situation_scope_keys", ["?"]))
                or probe.get("gold") not in probe.get("options", []) or any(o not in catalog["options"]
                                                                            for o in probe["options"])):
            problems.append(f"probe {pid!r}: bad fields")
    return problems


def replay_gold(episode):
    """Check one episode against the protocol and return its teacher-forced steps; raise ValueError on problems."""
    problems = check_structure(episode)
    if problems:
        raise ValueError(f"{episode.get('episode_id')}: " + "; ".join(problems))
    catalogs = catalogs_of(episode)
    steps, states = [], {}
    try:
        for step in gold_trajectory(episode):
            event, gold = step["event"], step["event"]["gold"]
            eid = event["event_id"]
            if not category_matches(gold["category"], step["changes"]):
                problems.append(f"{eid}: change {step['changes']} does not fit {gold['category']}")
            if (gold["decision"] == "clarify") != (gold["category"] == "clarify"):
                problems.append(f"{eid}: decision {gold['decision']} does not fit {gold['category']}")
            expected = canonical_state(gold["state_after"], catalogs)
            for arm in ARMS:
                if step["rejections"][arm]:
                    problems.append(f"{eid}: gold {arm} output rejected ({step['rejections'][arm]})")
                read, unmatched = READERS[arm](step["after_views"][arm], catalogs)
                if unmatched or read != expected:
                    problems.append(f"{eid}: {arm} memory does not read back as the gold state")
            steps.append({"event_id": eid, "category": gold["category"],
                          "inputs": {arm: policy_input(step["before"][arm].view(), event) for arm in ARMS},
                          "outputs": step["outputs"]})
            states[eid] = expected
    except (KeyError, ValueError) as exc:
        raise ValueError(f"{episode['episode_id']}: gold path cannot be projected ({exc!r}); " + "; ".join(problems))
    for probe in episode.get("probes", []):
        state = states[probe["after_event"]]
        entry = state[probe["attribute"]]
        applicable = [k for k, exc in entry["exceptions"].items()
                      if k in probe["situation_scope_keys"] and covers(exc["validity"], probe["date"])]
        if len(applicable) > 1:
            problems.append(f"probe {probe['probe_id']}: more than one exception applies")
        elif oracle_answer(state, probe) != probe["gold"]:
            problems.append(f"probe {probe['probe_id']}: gold {probe['gold']!r} disagrees with the state")
    if problems:
        raise ValueError(f"{episode['episode_id']}: " + "; ".join(problems))
    return steps


def sft_rows(episode):
    """Teacher-forced SFT rows for both arms; train on system, prompt and completion only."""
    rows = []
    for step in replay_gold(episode):
        for arm in ARMS:
            rows.append({"id": f"{episode['episode_id']}/{step['event_id']}/{arm}", "arm": arm,
                         "episode_id": episode["episode_id"], "event_id": step["event_id"],
                         "split": episode.get("split"), "category": step["category"],
                         "system": POLICY_INSTRUCTIONS[arm], "prompt": canon(step["inputs"][arm]),
                         "completion": canon(step["outputs"][arm])})
    return rows


def read_episodes(path):
    """Episodes from a JSONL file, or from a JSON file holding one episode or a list of them."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        whole = json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    return whole if isinstance(whole, list) else [whole]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Protocol v1 tools: gold replay checks and SFT export.")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="replay gold for every episode in the given JSONL files")
    check.add_argument("files", nargs="+")
    export = sub.add_parser("export-sft", help="write teacher-forced SFT rows for both arms")
    export.add_argument("files", nargs="+")
    export.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    failed, total = 0, 0
    if args.command == "check":
        for path in args.files:
            for episode in read_episodes(path):
                total += 1
                try:
                    replay_gold(episode)
                except ValueError as exc:
                    failed += 1
                    print(f"FAIL {exc}")
        print(json.dumps({"episodes": total, "failed": failed}))
        return 1 if failed else 0
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for path in args.files:
        rows = {arm: [] for arm in ARMS}
        for episode in read_episodes(path):
            for row in sft_rows(episode):
                rows[row["arm"]].append(row)
        for arm, arm_rows in rows.items():
            target = out / f"{Path(path).stem}_{arm}_sft.jsonl"
            target.write_text("".join(canon(r) + "\n" for r in arm_rows), encoding="utf-8")
            print(f"wrote {len(arm_rows)} rows to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
