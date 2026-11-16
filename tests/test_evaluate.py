import contextlib
import io
import json
import unittest

from scope_memory.evaluate import (NOOP_OUTPUT, main, noop_policy, parse_output, rollout, score_rollouts,
                                   self_check, summarize_rollouts, summarize_teacher_forced, teacher_forced)
from scope_memory.paths import FIXTURES
from scope_memory.protocol import canon, replay_gold

EPISODE = json.loads((FIXTURES / "protocol_episode.json").read_text())


def metric(report, name):
    m = report["metrics"][name]
    return m["count"], m["denominator"]


def gold_completions(arm):
    return {f"fx-0001/{s['event_id']}/{arm}": canon(s["outputs"][arm]) for s in replay_gold(EPISODE)}


class EvaluateTests(unittest.TestCase):
    def test_self_check_gold_is_perfect_and_noop_is_not(self):
        report = self_check([EPISODE], bootstrap=50)
        for arm in ("scope", "crud"):
            self.assertEqual(metric(report[f"teacher_forced_gold_{arm}"], "row_correct"), (7, 7))
            self.assertEqual(metric(report["rollout_gold"][arm], "qa_accuracy"), (9, 9))
            self.assertEqual(metric(report["rollout_noop"][arm], "qa_accuracy"), (3, 9))
        self.assertEqual(report["rollout_gold"]["scope_minus_crud"]["all"]["difference"], 0.0)

    def test_noop_predictions_teacher_forced(self):
        noop = {f"fx-0001/e{i}/scope": canon(NOOP_OUTPUT["scope"]) for i in range(1, 8)}
        report = summarize_teacher_forced(teacher_forced([EPISODE], "scope", noop), bootstrap=50)
        self.assertEqual(metric(report, "row_correct"), (1, 7))
        self.assertEqual(metric(report, "missed_update"), (1, 1))
        self.assertEqual(metric(report, "false_overwrite"), (0, 6))
        self.assertEqual(metric(report, "spurious_write"), (0, 2))
        self.assertEqual(metric(report, "clarify_recall"), (0, 1))

    def test_overwrite_invalid_and_rejected_outputs(self):
        preds = gold_completions("scope")
        preds["fx-0001/e1/scope"] = canon({"decision": "resolved", "actions": [{
            "operation": "REVISE", "target_id": "m1", "value": "regular coffee", "scope": "general",
            "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e1"]}]})
        preds["fx-0001/e2/scope"] = "I think nothing changes."
        preds["fx-0001/e3/scope"] = canon({"decision": "resolved", "actions": [
            {"operation": "RETIRE", "target_id": "m42", "evidence_ids": ["e3"]}]})
        scored = {s["event_id"]: s for s in teacher_forced([EPISODE], "scope", preds)}
        self.assertTrue(scored["e1"]["general_changed"])
        self.assertFalse(scored["e1"]["state_correct"])
        self.assertEqual((scored["e2"]["status"], scored["e2"]["reason"]), ("invalid", "not_json"))
        self.assertEqual((scored["e3"]["status"], scored["e3"]["reason"]), ("rejected", "unknown_target"))
        report = summarize_teacher_forced(list(scored.values()), bootstrap=50)
        self.assertEqual(metric(report, "false_overwrite"), (1, 6))
        self.assertEqual(metric(report, "invalid_or_rejected"), (2, 7))

    def test_crud_free_text_is_uninterpretable_not_a_crash(self):
        preds = gold_completions("crud")
        preds["fx-0001/e1/crud"] = canon({"decision": "resolved", "operations": [
            {"op": "ADD", "text": "Coffee in exam weeks, please."}]})
        scored = {s["event_id"]: s for s in teacher_forced([EPISODE], "crud", preds)}
        self.assertEqual(scored["e1"]["status"], "uninterpretable")
        self.assertFalse(scored["e1"]["general_changed"])
        self.assertTrue(scored["e1"]["wrote"])

    def test_answer_agent_answers_and_paired_difference(self):
        trajectories = [rollout(EPISODE, "scope", lambda a, s, p, c: gold_completions("scope")[f"fx-0001/{c['event_id']}/scope"]),
                        rollout(EPISODE, "crud", noop_policy)]
        answers = {f"fx-0001/{p['probe_id']}/scope": p["gold"] for p in EPISODE["probes"]}
        answers.update({f"fx-0001/{p['probe_id']}/crud": "green tea" for p in EPISODE["probes"]})
        report = summarize_rollouts(score_rollouts([EPISODE], trajectories, answers), bootstrap=50)
        self.assertEqual(report["scope"]["reader"], "answer_agent")
        self.assertEqual(metric(report["scope"], "qa_accuracy"), (9, 9))
        self.assertEqual(metric(report["crud"], "qa_accuracy"), (2, 9))
        self.assertAlmostEqual(report["scope_minus_crud"]["all"]["difference"], round(1 - 2 / 9, 4))

    def test_parse_output_accepts_fences(self):
        self.assertEqual(parse_output("```json\n{\"a\": 1}\n```"), ({"a": 1}, "fenced"))
        self.assertEqual(parse_output(None), (None, "missing"))

    def test_cli_self_check(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            main(["self-check", "--data", str(FIXTURES / "protocol_episode.json"), "--bootstrap", "20"])
        report = json.loads(buffer.getvalue())
        self.assertEqual(report["teacher_forced_gold_crud"]["metrics"]["row_correct"]["rate"], 1.0)


class RolloutWriteTests(unittest.TestCase):
    def test_write_metrics_along_own_memory(self):
        from scope_memory.evaluate import ROLLOUT_WRITE_METRICS, gold_policy, rollout_write_rows, summarize
        gold = [rollout(EPISODE, arm, gold_policy([EPISODE])) for arm in ("scope", "crud")]
        rows = rollout_write_rows([EPISODE], gold)
        for arm in ("scope", "crud"):
            m = summarize([r for r in rows if r["arm"] == arm], ROLLOUT_WRITE_METRICS, "category", 20)
            self.assertEqual(metric({"metrics": m}, "rollout_false_overwrite"), (0, 6))
            self.assertEqual(metric({"metrics": m}, "rollout_state_matches_gold"), (7, 7))
        m = summarize(rollout_write_rows([EPISODE], [rollout(EPISODE, "scope", noop_policy)]), ROLLOUT_WRITE_METRICS,
                      "category", 20)
        self.assertEqual(metric({"metrics": m}, "rollout_missed_update"), (1, 1))

    def test_incomplete_pairing_blocks_difference(self):
        from scope_memory.evaluate import gold_policy
        gold = [rollout(EPISODE, arm, gold_policy([EPISODE])) for arm in ("scope", "crud")]
        scored = [s for s in score_rollouts([EPISODE], gold) if s["id"] != "fx-0001/p1/crud"]
        report = summarize_rollouts(scored, bootstrap=20)
        self.assertFalse(report["pairing_complete"])
        self.assertNotIn("scope_minus_crud", report)


if __name__ == "__main__":
    unittest.main()
