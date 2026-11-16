import copy
import json
import unittest

from scope_memory.paths import FIXTURES
from scope_memory.protocol import (CrudMemory, ScopeMemory, catalogs_of, gold_trajectory, oracle_answer,
                                   read_crud_state, replay_gold, sft_rows)


def fixture():
    return json.loads((FIXTURES / "protocol_episode.json").read_text())


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.episode = fixture()
        self.steps = list(gold_trajectory(self.episode))

    def test_fixture_replays_for_both_arms(self):
        steps = replay_gold(self.episode)
        self.assertEqual([s["category"] for s in steps],
                         ["scoped_exception", "stable_preference", "exception_revision", "scoped_exception",
                          "clarify", "general_update", "exception_retirement"])
        self.assertEqual(steps[4]["outputs"]["scope"], {"decision": "clarify", "actions": [{"operation": "NOOP"}]})

    def test_evidence_identical_and_memory_arm_specific(self):
        for step in replay_gold(self.episode):
            scope, crud = step["inputs"]["scope"], step["inputs"]["crud"]
            self.assertEqual(json.dumps(scope["event"], sort_keys=True), json.dumps(crud["event"], sort_keys=True))
            self.assertEqual(set(scope), {"memory", "event"})
            self.assertTrue(all(set(r) == {"id", "text"} for r in crud["memory"]))

    def test_exception_revision_matches_outline_example(self):
        view = self.steps[2]["after_views"]["scope"]
        exam = next(r for r in view if r["scope"] == "exam weeks")
        self.assertEqual(exam["value"], "decaf coffee")
        self.assertEqual(exam["relations"], [{"type": "EXCEPTION_TO", "target": "m1"}, {"type": "REPLACES", "target": "m3"}])
        self.assertNotIn("m3", {r["memory_id"] for r in view})

    def test_general_revision_repoints_exceptions(self):
        view = self.steps[5]["after_views"]["scope"]
        general = next(r for r in view if r["attribute"] == "afternoon drink" and r["scope"] == "general")
        exam = next(r for r in view if r["scope"] == "exam weeks")
        self.assertEqual(general["value"], "sparkling water")
        self.assertIn({"type": "EXCEPTION_TO", "target": general["memory_id"]}, exam["relations"])

    def test_illegal_scope_outputs_are_rejected_without_change(self):
        memory = copy.deepcopy(self.steps[3]["before"]["scope"])
        before = memory.view()
        exception = {"operation": "ADD", "attribute": "afternoon drink", "value": "decaf coffee", "scope": "weekends",
                     "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}],
                     "evidence_ids": ["e4"]}
        cases = {
            "unknown_target": {"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m99", "evidence_ids": ["e4"]}]},
            "retire_general": {"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m1", "evidence_ids": ["e4"]}]},
            "second_general": {"decision": "resolved", "actions": [{**exception, "scope": "general", "relations": []}]},
            "exception_needs_one_edge": {"decision": "resolved", "actions": [{**exception, "relations": []}]},
            "bad_evidence": {"decision": "resolved", "actions": [{**exception, "evidence_ids": ["e9"]}]},
            "clarify_with_writes": {"decision": "clarify", "actions": [exception]},
            "noop_not_alone": {"decision": "resolved", "actions": [{"operation": "NOOP"}, exception]},
            "bad_window": {"decision": "resolved", "actions": [{**exception, "validity": {"kind": "window", "from": "2027-05-01", "to": "2027-04-01"}}]},
            "exception_without_general": {"decision": "resolved", "actions": [{**exception, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}]}]},
        }
        for reason, output in cases.items():
            self.assertEqual(memory.apply(output, "e4", ["seed", "e1", "e2", "e3", "e4"])[0], reason)
            self.assertEqual(memory.view(), before)
        self.assertIsNone(memory.apply({"decision": "resolved", "actions": [exception]}, "e4", ["seed", "e4"])[0])

    def test_crud_allows_free_text_records_and_rejects_bad_ids(self):
        memory = copy.deepcopy(self.steps[0]["before"]["crud"])
        ok = {"decision": "resolved", "operations": [{"op": "ADD", "text": "On weekends I like hot chocolate."},
                                                     {"op": "ADD", "text": "During exams: strong coffee."}]}
        self.assertEqual(memory.apply(ok), (None, ["m3", "m4"]))
        self.assertEqual(len(memory.view()), 4)
        before = memory.view()
        self.assertEqual(memory.apply({"decision": "resolved", "operations": [{"op": "DELETE", "id": "m9"}]})[0],
                         "unknown_target")
        self.assertEqual(memory.apply({"decision": "clarify", "operations": ok["operations"]})[0], "clarify_with_writes")
        self.assertEqual(memory.view(), before)
        state, unmatched = read_crud_state(memory.view(), catalogs_of(self.episode))
        self.assertEqual(unmatched, ["m3", "m4"])

    def test_oracle_window_boundary_and_inheritance(self):
        probes = {p["probe_id"]: p for p in self.episode["probes"]}
        after_e4 = self.episode["events"][3]["gold"]["state_after"]
        self.assertEqual(oracle_answer(after_e4, probes["p5"]), "evening")
        self.assertEqual(oracle_answer(after_e4, probes["p6"]), "morning")
        after_e7 = self.episode["events"][6]["gold"]["state_after"]
        self.assertEqual(oracle_answer(after_e7, probes["p9"]), "sparkling water")

    def test_replay_rejects_inconsistent_gold(self):
        broken = fixture()
        broken["events"][1]["gold"]["category"] = "general_update"
        with self.assertRaisesRegex(ValueError, "does not fit general_update"):
            replay_gold(broken)
        broken = fixture()
        broken["probes"][5]["gold"] = "evening"
        with self.assertRaisesRegex(ValueError, "disagrees with the state"):
            replay_gold(broken)
        broken = fixture()
        broken["events"][0]["gold"]["evidence_message"] = 2
        with self.assertRaisesRegex(ValueError, "evidence_message"):
            replay_gold(broken)

    def test_instruction_examples_are_valid_for_their_arm(self):
        from scope_memory.protocol import EXAMPLE_OUTPUTS, POLICY_INSTRUCTIONS, canon, read_crud_state, read_scope_state
        catalogs = {"drink order": {"attribute": "drink order", "options": ["black coffee", "green tea"],
                                    "scopes": {"office": {"scope": "at the office", "aliases": []}}}}
        window = {"kind": "window", "from": "2030-03-01", "to": "2030-03-14"}
        expected = {"drink order": {"general": "black coffee",
                                    "exceptions": {"office": {"value": "green tea", "validity": window}}}}
        for arm, memory, reader in (("scope", ScopeMemory(), read_scope_state), ("crud", CrudMemory(), read_crud_state)):
            write, noop = EXAMPLE_OUTPUTS[arm]
            self.assertIn(canon(write), POLICY_INSTRUCTIONS[arm])
            self.assertIn(canon(noop), POLICY_INSTRUCTIONS[arm])
            memory.seed({"drink order": {"general": "black coffee", "exceptions": {}}}, catalogs)
            self.assertIsNone(memory.apply(write, "e9", ["seed", "e9"])[0])
            self.assertEqual(reader(memory.view(), catalogs), (expected, []))
            self.assertIsNone(memory.apply(noop, "e10", ["seed", "e9", "e10"])[0])

    def test_sft_rows_hide_gold(self):
        rows = sft_rows(self.episode)
        self.assertEqual(len(rows), 14)
        for row in rows:
            prompt = json.loads(row["prompt"])
            self.assertEqual(set(prompt), {"memory", "event"})
            for leak in ("category", "rationale", "state_after", "probe", "exam\": {"):
                self.assertNotIn(leak, row["prompt"])
            json.loads(row["completion"])


if __name__ == "__main__":
    unittest.main()
