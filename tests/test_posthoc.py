import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

from scope_memory import analysis, posthoc
from scope_memory.evaluate import (_read_keyed, gold_policy, noop_policy, rollout, summarize_teacher_forced,
                                   teacher_forced)
from scope_memory.paths import FIXTURES
from scope_memory.protocol import ARMS, sft_rows

EPISODE_PATH = FIXTURES / "protocol_episode.json"


def copies(spec):
    """Copies of the fixture episode under other episode ids and families."""
    out = []
    for episode_id, family in spec:
        episode = json.loads(EPISODE_PATH.read_text())
        episode["episode_id"], episode["family"] = episode_id, family
        out.append(episode)
    return out


def make_run(root, name, episodes, policy, answer):
    """A run directory like baseline.sbatch writes; answer(k, n, probe, arm) gives the Answer Agent's choice for probe n
    of episode k."""
    run = Path(root) / name
    run.mkdir()
    (run / "episodes.jsonl").write_text("".join(json.dumps(e) + "\n" for e in episodes))
    trajectories = [rollout(e, arm, policy) for e in episodes for arm in ARMS]
    (run / "trajectories.jsonl").write_text("".join(json.dumps(t) + "\n" for t in trajectories))
    rows = [{"id": f"{e['episode_id']}/{p['probe_id']}/{arm}", "answer": answer(k, n, p, arm), "raw": "Answer: x"}
            for k, e in enumerate(episodes) for arm in ARMS for n, p in enumerate(e["probes"])]
    (run / "answers.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    for arm in ARMS:
        predictions = [{"id": r["id"], "completion": policy(arm, None, None, {"episode_id": r["episode_id"],
                                                                             "event_id": r["event_id"]})}
                       for e in episodes for r in sft_rows(e) if r["arm"] == arm]
        (run / f"predictions_{arm}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in predictions))
    return analysis.load_run(run)


def right(k, n, probe, arm):
    return probe["gold"]


def wrong(k, n, probe, arm):
    return next(o for o in probe["options"] if o != probe["gold"])


def mixed(k, n, probe, arm):
    return right(k, n, probe, arm) if (n + k + (arm == "scope")) % 3 else wrong(k, n, probe, arm)


def crud_slips(k, n, probe, arm):
    return wrong(k, n, probe, arm) if arm == "crud" and (n + k) % 2 else right(k, n, probe, arm)


def write_cost(run, calls=10):
    measures = {m: {"calls": calls, "mean": 100.0 + i, "total": calls * (100 + i)}
                for i, m in enumerate(posthoc.COST_MEASURES)}
    arms = {arm: {**measures, "rejected_outputs": 0} for arm in ARMS}
    (Path(run["path"]) / "cost.json").write_text(json.dumps({"runs": {run["path"]: {"arms": arms}}}))


class PosthocTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.episodes = copies([("ep-a", "fam-1"), ("ep-b", "fam-1"), ("ep-c", "fam-2")])
        self.gold = gold_policy(self.episodes)

    def tearDown(self):
        self.tmp.cleanup()

    def run_(self, name, policy, answer):
        return make_run(self.root, name, self.episodes, policy, answer)

    def test_decomposition_adds_up_and_reproduces_the_report(self):
        sft = [self.run_("s0", self.gold, mixed), self.run_("s1", noop_policy, right)]
        gold = self.run_("gold", self.gold, crud_slips)
        out = posthoc.decompose(sft, gold, bootstrap=200)
        report = analysis.report({"sft": sft, "gold": [gold]}, bootstrap=200)
        for group, e in out["by_unit"]["episode"].items():
            self.assertAlmostEqual(e["total"]["mean"], e["format"]["mean"] + e["write"]["mean"], places=3)
            self.assertAlmostEqual(e["total"]["mean"], report["h1_sft_scope_minus_crud"][group]["difference"])
            self.assertEqual(e["total"]["ci95"], report["h1_sft_scope_minus_crud"][group]["ci95"])
            self.assertEqual(e["format"]["ci95"], report["scope_minus_crud"]["gold"][group]["ci95"])
            self.assertAlmostEqual(e["sft_scope"]["mean"], report["accuracy"]["sft"]["scope"][group]["accuracy"])
        self.assertGreater(out["by_unit"]["episode"]["all"]["format"]["mean"], 0)
        self.assertEqual((out["episodes"], out["families"]), (3, 2))
        self.assertEqual(out["by_unit"]["family"]["all"]["units"], 2)
        self.assertEqual(sum(f["probes"] for f in out["per_family"]), out["probes"])

    def test_cluster_means_resamples_families(self):
        run = self.run_("s0", self.gold, mixed)
        series = {"x": analysis.correctness([run], "scope")}
        out = posthoc.cluster_means(series, posthoc.probe_table(run["episodes"]), "family", groups=("all",),
                                    bootstrap=50, keep=True)
        self.assertEqual(out["all"]["units"], 2)
        self.assertEqual(len(out["all"]["x"]["draws"]), 50)
        for episode in run["episodes"]:
            episode["family"] = "one"
        one = posthoc.cluster_means(series, posthoc.probe_table(run["episodes"]), "family", groups=("all",),
                                    bootstrap=20)["all"]["x"]
        self.assertEqual(one["ci95"], [one["mean"], one["mean"]])

    def test_mechanism_matches_the_evaluator_and_checks_stored_files(self):
        good, never = self.run_("good", self.gold, right), self.run_("never", noop_policy, wrong)
        rows = {arm: [] for arm in ARMS}
        for run in (good, never):
            for arm in ARMS:
                mine = teacher_forced(run["episodes"], arm,
                                      _read_keyed(Path(run["path"]) / f"predictions_{arm}.jsonl", "completion"))
                rows[arm] += mine
                if run is never:
                    (Path(run["path"]) / f"eval_tf_{arm}.json").write_text(
                        json.dumps(summarize_teacher_forced(mine, bootstrap=20)))
        out = posthoc.mechanism([good, never], bootstrap=50)
        self.assertEqual(len(out["checks"]), 2)
        self.assertTrue(all(c["matches_eval_tf"] for c in out["checks"]))
        for arm in ARMS:
            expected = summarize_teacher_forced(rows[arm], bootstrap=20)
            for name, v in {**expected["metrics"], **expected["parse_failures"]}.items():
                self.assertEqual((out["metrics"][name][arm]["count"], out["metrics"][name][arm]["denominator"]),
                                 (v["count"], v["denominator"]), (arm, name))
        perfect = posthoc.mechanism([good], bootstrap=20)
        for arm in ARMS:
            self.assertEqual(perfect["metrics"]["structure_matches_gold"][arm]["rate"], 1.0)
            self.assertEqual(perfect["metrics"]["row_correct"][arm]["rate"], 1.0)
        self.assertEqual(perfect["metrics"]["row_correct"]["scope_minus_crud"]["difference"], 0.0)
        self.assertIn("clarify", perfect["by_category"]["row_correct"])
        stored = Path(never["path"]) / "eval_tf_scope.json"
        data = json.loads(stored.read_text())
        data["metrics"]["row_correct"]["count"] += 1
        stored.write_text(json.dumps(data))
        checks = posthoc.mechanism([never], bootstrap=20)["checks"]
        self.assertEqual({c["arm"]: c["matches_eval_tf"] for c in checks}, {"scope": False, "crud": True})

    def test_composition(self):
        split, other = self.root / "split.jsonl", self.root / "other.jsonl"
        split.write_text("".join(json.dumps(e) + "\n" for e in self.episodes))
        other.write_text(json.dumps(self.episodes[0]) + "\n")
        out = posthoc.composition([split, other])
        f = out["files"]["split"]
        self.assertEqual((f["episodes"], f["families"], f["two_attribute_episodes"]), (3, 2, 3))
        self.assertEqual(f["probes"], 3 * len(self.episodes[0]["probes"]))
        for key in ("probe_types", "qa_groups", "situation_records_at_probe"):
            self.assertEqual(sum(v["count"] for v in f[key].values()), f["probes"], key)
        self.assertEqual(sum(v["count"] for v in f["event_categories"].values()), f["events"])
        self.assertEqual(out["shared_families"], {"split & other": 1})

    def test_dev_vs_test_of_a_split_against_itself(self):
        sft, gold = [self.run_("s0", self.gold, mixed)], self.run_("gold", self.gold, crud_slips)
        out = posthoc.dev_vs_test(sft, gold, sft, gold, bootstrap=50)
        for unit in posthoc.UNITS:
            for parts in out["test_minus_dev"][unit].values():
                self.assertEqual([parts[p]["mean"] for p in posthoc.PARTS], [0.0, 0.0, 0.0])
        overall = out["splits"]["dev"]["by_unit"]["episode"]["all"]
        for mixes in out["standardised"].values():
            for m in mixes.values():
                self.assertAlmostEqual(sum(m["weights"].values()), 1.0, places=3)
                for part in posthoc.PARTS:
                    self.assertAlmostEqual(m[part]["mean"], overall[part]["mean"], places=3)
        self.assertNotIn("draws", json.dumps(out))
        spread = out["splits"]["test"]["family_spread"]
        self.assertEqual(spread["scope_ahead"] + spread["crud_ahead"] + spread["tied"], 2)

    def test_cost_pools_runs(self):
        a, b = self.run_("a", noop_policy, right), self.run_("b", noop_policy, right)
        write_cost(a, calls=10)
        write_cost(b, calls=30)
        out = posthoc.cost([a["path"], b["path"]])
        self.assertEqual(out["arms"]["scope"]["policy_input_tokens"], {"calls": 40, "total": 4000, "mean": 100.0})
        self.assertEqual(out["arms"]["crud"]["rejected_outputs"], 0)
        self.assertEqual(out["runs"], [Path(a["path"]).as_posix(), Path(b["path"]).as_posix()])

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "matplotlib is not installed")
    def test_figures_and_tables_from_the_reports(self):
        from scope_memory import figures
        runs = {"noop": [self.run_("noop", noop_policy, wrong)], "zero_shot": [self.run_("zero", noop_policy, mixed)],
                "six_shot": [self.run_("six", self.gold, mixed)],
                "sft": [self.run_("s0", self.gold, mixed), self.run_("s1", self.gold, right)],
                "gold": [self.run_("gold", self.gold, crud_slips)]}
        for run in runs["sft"]:
            write_cost(run)
        results = self.root / "results"
        (results / "test_p12").mkdir(parents=True)
        (results / "posthoc").mkdir()
        (results / "test_p12" / "report.json").write_text(json.dumps(analysis.report(runs, bootstrap=20)))
        data = self.root / "split.jsonl"
        data.write_text("".join(json.dumps(e) + "\n" for e in self.episodes))
        reports = {"dev_vs_test": posthoc.dev_vs_test(runs["sft"], runs["gold"][0], runs["sft"], runs["gold"][0],
                                                      bootstrap=20),
                   "cost_test": {"conditions": {"sft": posthoc.cost([r["path"] for r in runs["sft"]])}},
                   "mechanism_test": posthoc.mechanism(runs["sft"], bootstrap=20),
                   "mechanism_dev": posthoc.mechanism(runs["sft"], bootstrap=20),
                   "composition": posthoc.composition([data])}
        for name, report in reports.items():
            (results / "posthoc" / f"{name}.json").write_text(json.dumps(report))
        with contextlib.redirect_stdout(io.StringIO()):
            figures.main(["--results", str(results), "--out", str(self.root / "figures")])
        made = sorted(p.name for p in (self.root / "figures").iterdir())
        self.assertEqual(len(made), 11)
        self.assertIn("## Table 4.", (self.root / "figures" / "tables.md").read_text(encoding="utf-8"))
        # with the read-time reports: two more figures and Tables 8 and 9
        from scope_memory import readtime
        from tests.test_readtime import display_run, history_run, stored_scope
        history = history_run(self.root, "history", self.episodes, mixed)
        displays = [display_run(self.root, f"d_{Path(r['path']).name}", r,
                                {"replay": stored_scope(r), "compact": right, "sentences": crud_slips})
                    for r in runs["sft"] + runs["gold"]]
        a = readtime.experiment_a(history, runs["sft"], runs["gold"][0], runs["noop"][0],
                                  [Path(r["path"]) / "cost.json" for r in runs["sft"]], bootstrap=20)
        b = readtime.experiment_b(displays, runs["sft"], runs["gold"][0], bootstrap=20)
        for split in ("test", "dev"):
            (results / "posthoc" / f"readtime_a_{split}.json").write_text(json.dumps(a))
            (results / "posthoc" / f"readtime_b_{split}.json").write_text(json.dumps(b))
        with contextlib.redirect_stdout(io.StringIO()):
            figures.main(["--results", str(results), "--out", str(self.root / "figures_rt")])
        made = sorted(p.name for p in (self.root / "figures_rt").iterdir())
        self.assertEqual(len(made), 15)
        self.assertIn("fig7_memory_display.png", made)
        self.assertIn("## Table 9.", (self.root / "figures_rt" / "tables.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
