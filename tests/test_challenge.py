import importlib.util
import unittest

from scope_memory.analysis import stressor_of
from scope_memory.paths import ROOT
from scope_memory.protocol import read_episodes, replay_gold

CHALLENGE = ROOT / "training" / "challenge_v1"


def builder():
    spec = importlib.util.spec_from_file_location("challenge_build", CHALLENGE / "build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChallengeSetTests(unittest.TestCase):
    """training/challenge_v1: the committed data replays and matches a rebuild from the hand-written episodes."""

    def test_data_replays_and_matches_a_rebuild(self):
        episodes = read_episodes(CHALLENGE / "data" / "challenge.jsonl")
        for episode in episodes:
            replay_gold(episode)
            self.assertEqual(episode["split"], "challenge")
            self.assertIsNotNone(stressor_of(episode))
        build = builder()
        rebuilt, problems = build.build()
        self.assertEqual(problems, [])
        for path, data in build.outputs(rebuilt).items():
            self.assertEqual(path.read_bytes(), data, path.name)

    def test_options_put_the_confusable_values_first(self):
        build = builder()
        state = {"a": {"general": "g", "exceptions": {"k": {"value": "x", "validity": {"kind": "persistent"}},
                                                      "j": {"value": "y", "validity": {"kind": "persistent"}}}}}
        catalog = {"options": ["g", "x", "y", "z", "old", "w"]}
        options = build.pick_options("x", "a", "k", state, {("a", "k"): ["old"]}, catalog, "p1")
        self.assertEqual(sorted(options), ["g", "old", "x", "y"])
        self.assertEqual(options, build.pick_options("x", "a", "k", state, {("a", "k"): ["old"]}, catalog, "p1"))


if __name__ == "__main__":
    unittest.main()
