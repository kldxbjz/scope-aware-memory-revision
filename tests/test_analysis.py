import json
import tempfile
import unittest
from pathlib import Path

from scope_memory import analysis
from scope_memory.evaluate import _paired_qa, gold_policy, noop_policy, rollout
from scope_memory.paths import FIXTURES
from scope_memory.protocol import ARMS, CATEGORIES, catalogs_of, sft_rows

EPISODE_PATH = FIXTURES / "protocol_episode.json"


def fixture():
    return json.loads(EPISODE_PATH.read_text())


def make_run(root, name, policy, answer):
    """A run directory like baseline.sbatch writes, for the fixture episode."""
    episode = fixture()
    run = Path(root) / name
    run.mkdir()
    (run / "episodes.jsonl").write_text(json.dumps(episode) + "\n")
    trajectories = [rollout(episode, arm, policy) for arm in ARMS]
    (run / "trajectories.jsonl").write_text("".join(json.dumps(t) + "\n" for t in trajectories))
    rows = [{"id": f"{episode['episode_id']}/{p['probe_id']}/{arm}", "answer": answer(n, p, arm), "raw": "Answer: x"}
            for arm in ARMS for n, p in enumerate(episode["probes"])]
    (run / "answers.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    for arm in ARMS:
        predictions = [{"id": r["id"], "completion": policy(arm, None, None, {"episode_id": r["episode_id"],
                                                                             "event_id": r["event_id"]})}
                       for r in sft_rows(episode) if r["arm"] == arm]
        (run / f"predictions_{arm}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in predictions))
    return analysis.load_run(run)


def right(n, probe, arm):
    return probe["gold"]


def wrong(n, probe, arm):
    return next(o for o in probe["options"] if o != probe["gold"])


def mixed(n, probe, arm):
    return right(n, probe, arm) if (n + (arm == "scope")) % 3 else wrong(n, probe, arm)


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.gold = gold_policy([fixture()])

    def tearDown(self):
        self.tmp.cleanup()

    def test_paired_matches_the_evaluator(self):
        run = make_run(self.tmp.name, "mixed", self.gold, mixed)
        info = analysis.probe_info(run["episodes"])
        mine = analysis.paired(analysis.correctness([run], "scope"), analysis.correctness([run], "crud"), info,
                               bootstrap=200)
        theirs = _paired_qa(list(run["scored"].values()), 200, 0)
        for group in ("all",) + tuple(g for g in theirs if g != "all"):
            self.assertAlmostEqual(mine[group]["difference"], theirs[group]["difference"])
            self.assertEqual(mine[group]["ci95"], theirs[group]["ci95"])
        self.assertIn("type_boundary", mine)
        self.assertEqual(mine["all"]["probes"], len(fixture()["probes"]))

    def test_report_pools_seeds_and_compares_conditions(self):
        good = make_run(self.tmp.name, "good", self.gold, right)
        half = make_run(self.tmp.name, "half", self.gold, mixed)
        bad = make_run(self.tmp.name, "bad", noop_policy, wrong)
        out = analysis.report({"sft": [good, half], "zero_shot": [bad], "gold": [good]}, bootstrap=50)
        n = len(fixture()["probes"])
        pooled = {arm: (n + sum(mixed(i, p, arm) == p["gold"] for i, p in enumerate(fixture()["probes"]))) / (2 * n)
                  for arm in ARMS}
        for arm in ARMS:
            self.assertAlmostEqual(out["accuracy"]["sft"][arm]["all"]["accuracy"], round(pooled[arm], 4))
            self.assertEqual(out["accuracy"]["zero_shot"][arm]["all"]["accuracy"], 0.0)
            self.assertAlmostEqual(out["h2_sft_minus_prompt"][arm]["sft_minus_zero_shot"]["all"]["difference"],
                                   round(pooled[arm], 4))
        self.assertAlmostEqual(out["h1_sft_scope_minus_crud"]["all"]["difference"],
                               round(pooled["scope"] - pooled["crud"], 4))
        self.assertEqual(out["conditions"], {"sft": 2, "zero_shot": 1, "gold": 1})

    def test_memory_classes(self):
        good = make_run(self.tmp.name, "good", self.gold, right)
        out = analysis.memory_classes([good], bootstrap=20)
        for arm in ARMS:
            self.assertEqual(set(out["classes"][arm]), {"matches_gold"})
        never = make_run(self.tmp.name, "never", noop_policy, wrong)
        classes = analysis.memory_classes([never], bootstrap=20)["classes"]
        for arm in ARMS:
            self.assertTrue({"same_structure", "different_structure"} <= set(classes[arm]))
            self.assertNotIn("unreadable", classes[arm])

    def test_attribute_class_cases(self):
        episode = fixture()
        catalogs = catalogs_of(episode)
        gold = {"general": "green tea", "exceptions": {"exam": {"value": "regular coffee",
                                                                "validity": {"kind": "persistent"}}}}
        crud = ["For afternoon drink, the user prefers green tea.",
                "For afternoon drink when during exams, the user prefers regular coffee."]
        view = [{"id": f"m{i}", "text": t} for i, t in enumerate(crud)]
        self.assertEqual(analysis.attribute_class(view, "crud", catalogs, "afternoon drink", gold), "matches_gold")
        self.assertEqual(analysis.attribute_class(view + [{"id": "m9", "text": crud[0]}], "crud", catalogs,
                                                  "afternoon drink", gold), "different_structure")
        self.assertEqual(analysis.attribute_class(view + [{"id": "m9", "text": "I like tea."}], "crud", catalogs,
                                                  "afternoon drink", gold), "unreadable")
        other = [{"id": "m9", "text": "Groceries: grocery delivery window is mornings, mostly."}]
        self.assertEqual(analysis.attribute_class(view + other, "crud", catalogs, "afternoon drink", gold),
                         "matches_gold")
        scope = [{"attribute": "afternoon drink", "value": "green tea", "scope": "general",
                  "validity": {"kind": "persistent"}},
                 {"attribute": "afternoon drink", "value": "decaf", "scope": "exam week",
                  "validity": {"kind": "persistent"}}]
        self.assertEqual(analysis.attribute_class(scope, "scope", catalogs, "afternoon drink", gold), "same_structure")
        scope[1]["scope"] = "the library"
        self.assertEqual(analysis.attribute_class(scope, "scope", catalogs, "afternoon drink", gold), "unreadable")

    def test_structure_of_gold_predictions(self):
        out = analysis.structure([make_run(self.tmp.name, "good", self.gold, right)])
        for arm in ARMS:
            self.assertEqual(out[arm]["structure_matches_gold"]["rate"], 1.0)
            self.assertEqual(out[arm]["top_mismatches"], [])
            self.assertTrue(all(k.endswith(":listed") for k in out[arm]["written_forms"]))

    def test_error_sample_packet(self):
        run = make_run(self.tmp.name, "bad", noop_policy, wrong)
        sample = analysis.error_sample(run, "scope", 3, seed=0)
        self.assertEqual(sample["sampled"], 3)
        self.assertEqual(sample["wrong_probes"], len(fixture()["probes"]))
        self.assertEqual([i["id"] for i in sample["items"]], sorted(i["id"] for i in sample["items"]))
        for item in sample["items"]:
            probe = next(p for p in fixture()["probes"] if item["id"].split("/")[1] == p["probe_id"])
            self.assertEqual(item["events"][-1]["event_id"], probe["after_event"])
        self.assertEqual(analysis.error_sample(run, "scope", 3, seed=0), sample)
        text = analysis.error_packet_markdown(sample)
        self.assertIn("## 3.", text)
        self.assertIn("Gold memory at the probe", text)

    def test_label_audit_round_trip(self):
        items, key = analysis.label_sample([EPISODE_PATH], per_category=1, seed=0)
        self.assertEqual(len(items), len(CATEGORIES))
        self.assertNotIn("gold", json.dumps(items))
        events = {ev["event_id"]: ev["gold"]["category"] for ev in fixture()["events"]}
        gold = {i: events[v["event_id"]] for i, v in key.items()}
        root = Path(self.tmp.name)
        (root / "key.json").write_text(json.dumps(key))
        first = sorted(gold)[0]
        for name, labels in (("a", gold), ("b", {**gold, first: "clarify" if gold[first] != "clarify" else "general_update"})):
            template = analysis.label_template(sorted(gold), "category", CATEGORIES)
            template["annotator"] = name
            for item in template["items"]:
                item["category"] = labels[item["id"]]
            (root / f"{name}.json").write_text(json.dumps(template))
        out = analysis.agreement_report([root / "a.json", root / "b.json"], root / "key.json")
        self.assertEqual(out["against_gold"]["a"]["agreement"], 1.0)
        self.assertEqual(out["against_gold"]["b"]["disagreements"][0]["id"], first)
        self.assertAlmostEqual(out["pairwise"]["a vs b"]["agreement"], round(5 / 6, 4))

    def test_kappa(self):
        self.assertEqual(analysis.agreement({1: "x", 2: "x", 3: "y", 4: "y"}, {1: "x", 2: "y", 3: "y", 4: "y"}),
                         {"items": 4, "agreement": 0.75, "kappa": 0.5})


if __name__ == "__main__":
    unittest.main()
