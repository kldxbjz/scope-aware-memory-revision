import json
import unittest
from scope_memory.paths import FIXTURES
from scope_memory.replay import Memory, replay

class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.ep = json.loads((FIXTURES / "toy_episode.json").read_text())

    def test_oracle_preserves_exception(self):
        r = replay(self.ep, True)
        self.assertEqual((r["qa_correct"], r["qa_total"], r["false_overwrites"]), (6,6,0))

    def test_scope_blind_detectable_overwrite(self):
        r = replay(self.ep, False)
        self.assertEqual((r["qa_correct"], r["qa_total"], r["false_overwrites"]), (4,6,1))
        self.assertEqual(r["overwrite_opportunities"], 1)

    def test_prefix_has_no_future_state(self):
        r = replay({"events": self.ep["events"][:1]}, True)
        self.assertTrue(all(p["prediction"] == "tea" for p in r["trace"]))

    def test_unordered_events_rejected(self):
        with self.assertRaises(ValueError):
            replay({"events": list(reversed(self.ep["events"]))}, True)

    def test_delete_and_noop(self):
        m = Memory(True)
        m.apply({"time":1,"attribute":"x","scope":"*","action":"add","value":"a"})
        m.apply({"time":2,"attribute":"x","scope":"*","action":"noop","value":None})
        self.assertEqual(m.answer("x"), "a")
        m.apply({"time":3,"attribute":"x","scope":"*","action":"delete","value":None})
        self.assertIsNone(m.answer("x"))

    def test_empty_denominators(self):
        r = replay({"events":[]},True)
        self.assertIsNone(r["qa_accuracy"])
        self.assertIsNone(r["false_overwrite_rate"])

if __name__ == "__main__":
    unittest.main()
