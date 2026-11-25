import contextlib
import copy
import io
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from scope_memory import readtime
from scope_memory.evaluate import answer_prompt, gold_policy, noop_policy, rollout
from scope_memory.protocol import GENERAL, CrudMemory, catalogs_of
from tests.test_posthoc import copies, crud_slips, make_run, mixed, right, wrong, write_cost


def write_jsonl(path, rows):
    Path(path).write_text("".join(json.dumps(r) + "\n" for r in rows))


def history_run(root, name, episodes, answer):
    """A run directory like reread.py --history writes; answer(k, n, probe, arm) gives the choice for probe n of
    episode k."""
    run = Path(root) / name
    run.mkdir()
    (run / "run_config.json").write_text(json.dumps({"kind": "history"}))
    write_jsonl(run / "episodes.jsonl", episodes)
    write_jsonl(run / "answers_history.jsonl",
                [{"id": f"{e['episode_id']}/{p['probe_id']}/history", "answer": answer(k, n, p, None),
                  "raw": "It holds.\nAnswer: x", "input_tokens": 500, "output_tokens": 20, "events": 1}
                 for k, e in enumerate(episodes) for n, p in enumerate(e["probes"])])
    (run / "history_check.json").write_text(json.dumps({"prompts": 1}))
    return readtime.load_readtime(run)


def display_run(root, name, source, answers):
    """A run directory like reread.py --from-run writes; answers[condition](k, n, probe, arm) gives the choices."""
    run = Path(root) / name
    run.mkdir()
    (run / "run_config.json").write_text(json.dumps({"kind": "display", "from_run": source["path"]}))
    write_jsonl(run / "episodes.jsonl", source["episodes"])
    for c in readtime.DISPLAYS:
        write_jsonl(run / f"answers_{c}.jsonl",
                    [{"id": f"{e['episode_id']}/{p['probe_id']}/{c}", "answer": answers[c](k, n, p, "scope"),
                      "raw": "Answer: x", "input_tokens": 300, "output_tokens": 20, "memory_tokens": 100}
                     for k, e in enumerate(source["episodes"]) for n, p in enumerate(e["probes"])])
    (run / "display_check.json").write_text(json.dumps({"bad_edges": 0, "replaces_active": 0}))
    return readtime.load_readtime(run)


def stored_scope(run):
    """The stored scope-arm answer of run as an answer function."""
    table = {k.rsplit("/", 1)[0]: s["answer"] for k, s in run["scored"].items() if s["arm"] == "scope"}
    by_position = {}
    for k, e in enumerate(run["episodes"]):
        for n, p in enumerate(e["probes"]):
            by_position[(k, n)] = table[f"{e['episode_id']}/{p['probe_id']}"]
    return lambda k, n, probe, arm: by_position[(k, n)]


class PromptTests(unittest.TestCase):
    def setUp(self):
        self.episode = copies([("ep-a", "fam-1")])[0]
        for ev in self.episode["events"]:
            for m in ev["dialogue"]:
                m["content"] += f" <{ev['event_id']}>"
            ev["gold"]["note"] = "GOLD-ONLY"

    def test_history_prompt_holds_the_start_and_the_conversations_up_to_the_probe(self):
        e = self.episode
        seed = CrudMemory()
        seed.seed(e["initial_state"], catalogs_of(e))
        order = [ev["event_id"] for ev in e["events"]]
        for probe in e["probes"]:
            prompt = readtime.history_prompt(e, probe)
            for r in seed.view():
                self.assertIn(f"- {r['text']}", prompt)
            last = order.index(probe["after_event"])
            for k, event_id in enumerate(order):
                self.assertEqual(f"<{event_id}>" in prompt, k <= last, (probe["probe_id"], event_id))
            self.assertNotIn("GOLD-ONLY", prompt)
            tail = answer_prompt([], probe, readtime.READER).split("\n")[3:6]
            self.assertEqual(prompt.split("\n")[-6:-3], tail)
            self.assertTrue(prompt.endswith(readtime.HISTORY_REPLY))
            self.assertEqual(prompt.count("Conversation on "), last + 1)
        with self.assertRaises(ValueError):
            readtime.events_until(e, "missing")

    def test_display_prompts_change_only_the_memory_block(self):
        e = self.episode
        scope = rollout(e, "scope", gold_policy([e]))
        crud = rollout(e, "crud", gold_policy([e]))
        seen_window = False
        for probe in e["probes"]:
            view = scope["snapshots"][probe["after_event"]]
            original = answer_prompt(view, probe, readtime.READER)
            self.assertEqual(readtime.display_prompt(view, probe, "replay"), original)
            tail = original.split("\n\nDate: ")[1]
            for condition in ("compact", "sentences"):
                prompt = readtime.display_prompt(view, probe, condition)
                self.assertEqual(prompt.split("\n\nDate: ")[1], tail)
                self.assertTrue(prompt.startswith("Memory records:\n"))
            compact = readtime.render_compact(view)
            self.assertNotIn("memory_id", compact)
            self.assertNotIn("evidence", compact)
            for r in view:
                self.assertIn(r["value"], compact)
                if r["scope"] != GENERAL:
                    self.assertIn(f"- when {r['scope']}: {r['value']}", compact)
                if r["validity"]["kind"] == "window":
                    seen_window = True
                    self.assertIn(f"from {r['validity']['from']} through {r['validity']['to']}", compact)
            self.assertEqual(compact.count("- general: "), len({r["attribute"] for r in view}))
        self.assertTrue(seen_window)
        for event_id, view in scope["snapshots"].items():  # on gold memory both arms then show the same sentences
            mine = Counter(r["text"] for r in readtime.as_crud_view(view))
            self.assertEqual(mine, Counter(r["text"] for r in crud["snapshots"][event_id]))
        self.assertEqual(readtime.render_compact([]), "(none)")
        with self.assertRaises(ValueError):
            readtime.memory_block(view, "other")

    def test_display_check_counts_broken_links(self):
        e = self.episode
        scope = rollout(e, "scope", gold_policy([e]))
        total = Counter()
        for view in scope["snapshots"].values():
            total.update(readtime.display_check(view))
        self.assertEqual((total["bad_edges"], total["replaces_active"]), (0, 0))
        self.assertEqual(total["edges_ok"], total["situation"])
        self.assertGreater(total["situation"], 0)
        view = copy.deepcopy(next(v for v in scope["snapshots"].values() if any(r["scope"] != GENERAL for r in v)))
        situation = next(r for r in view if r["scope"] != GENERAL)
        situation["relations"] = [{"type": "EXCEPTION_TO", "target": "m999"},
                                  {"type": "REPLACES", "target": view[0]["memory_id"]}]
        counts = readtime.display_check(view)
        self.assertEqual((counts["bad_edges"], counts["replaces_active"]), (1, 1))


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.episodes = copies([("ep-a", "fam-1"), ("ep-b", "fam-1"), ("ep-c", "fam-2")])
        self.gold = gold_policy(self.episodes)

    def tearDown(self):
        self.tmp.cleanup()

    def run_(self, name, policy, answer):
        return make_run(self.root, name, self.episodes, policy, answer)

    def test_experiment_a(self):
        sft = [self.run_("s0", self.gold, mixed), self.run_("s1", noop_policy, right)]
        gold, noop = self.run_("gold", self.gold, right), self.run_("noop", noop_policy, wrong)
        for run in sft:
            write_cost(run, calls=10)
        history = history_run(self.root, "history", self.episodes, right)
        out = readtime.experiment_a(history, sft, gold, noop, [Path(r["path"]) / "cost.json" for r in sft],
                                    bootstrap=100)
        overall = out["by_unit"]["episode"]["all"]
        self.assertEqual(overall["history"]["mean"], 1.0)
        self.assertAlmostEqual(overall["history_minus_sft_scope"]["mean"], 1.0 - overall["sft_scope"]["mean"], places=4)
        self.assertEqual(overall["history_minus_gold_crud"]["mean"], 0.0)
        self.assertEqual(overall["noop_scope"]["mean"], 0.0)
        self.assertEqual(len(out["flips_per_seed"]), 4)
        for f in out["flips_per_seed"]:
            self.assertEqual(f["history_only"] + f["both"], out["probes"])
            self.assertEqual((f["memory_only"], f["neither"]), (0, 0))
            self.assertEqual(sum(c["probes"] for c in f["by_probe_type"].values()), out["probes"])
        self.assertEqual(out["cost_per_run"]["history"]["answer_input_tokens"], 500 * out["probes"])
        self.assertEqual(out["cost_per_run"]["scope"]["policy_calls"], 10)
        self.assertEqual(out["answer_line_missing"], 0)
        self.assertEqual(out["by_unit"]["family"]["all"]["units"], 2)
        part = history_run(self.root, "part", self.episodes[:2], wrong)  # a smoke run: fewer episodes
        small = readtime.experiment_a(part, sft, gold, bootstrap=20)
        self.assertEqual(small["episodes"], 2)
        self.assertEqual(small["by_unit"]["episode"]["all"]["history"]["mean"], 0.0)
        self.assertNotIn("scope", small["cost_per_run"])

    def test_experiment_b(self):
        sft = [self.run_("s0", self.gold, mixed), self.run_("s1", self.gold, crud_slips)]
        gold = self.run_("gold", self.gold, crud_slips)
        displays = [display_run(self.root, f"d_{Path(r['path']).name}", r,
                                {"replay": stored_scope(r), "compact": right, "sentences": wrong})
                    for r in sft + [gold]]
        out = readtime.experiment_b(displays, sft, gold, bootstrap=100)
        for label in ("sft", "gold"):
            s = out["sets"][label]
            e = s["by_unit"]["episode"]["all"]
            self.assertEqual(e["replay_minus_original"]["mean"], 0.0)
            self.assertEqual(e["compact"]["mean"], 1.0)
            self.assertAlmostEqual(e["compact_minus_replay"]["mean"], 1.0 - e["replay"]["mean"], places=4)
            self.assertAlmostEqual(e["display_part"]["mean"] + e["content_part"]["mean"],
                                   e["original_minus_crud"]["mean"], places=4)
            for r in s["per_run"]:
                self.assertEqual(r["replay_same_answer"]["share"], 1.0)
                self.assertEqual((r["replay"]["lost"], r["replay"]["gained"]), (0, 0))
                self.assertEqual(r["sentences"]["gained"], 0)
            self.assertEqual(s["tokens"]["compact"]["memory_tokens"]["mean"], 100.0)
            self.assertEqual(s["display_check"], {"bad_edges": 0, "replaces_active": 0})
        self.assertEqual(out["sets"]["gold"]["by_unit"]["episode"]["all"]["original"]["mean"], 1.0)
        with self.assertRaises(ValueError):
            readtime.experiment_b(displays[:2], sft, gold, bootstrap=20)
        with self.assertRaises(ValueError):
            readtime.experiment_b(displays + displays[:1], sft, gold, bootstrap=20)

    def test_show_prints_the_prompts(self):
        data = self.root / "split.jsonl"
        write_jsonl(data, self.episodes)
        run = self.run_("s0", self.gold, right)
        probe = self.episodes[1]["probes"][3]
        key = f"{self.episodes[1]['episode_id']}/{probe['probe_id']}"
        for argv, expected in (
                (["show", "--data", str(data), "--probe", key], readtime.history_prompt(self.episodes[1], probe)),
                (["show", "--data", str(data), "--probe", key, "--run", run["path"], "--condition", "sentences"],
                 readtime.display_prompt(run["trajectories"][(self.episodes[1]["episode_id"], "scope")]["snapshots"]
                                         [probe["after_event"]], probe, "sentences"))):
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                readtime.main(argv)
            self.assertEqual(buffer.getvalue(), expected + "\n")


if __name__ == "__main__":
    unittest.main()
