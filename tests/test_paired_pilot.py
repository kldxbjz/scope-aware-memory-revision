import unittest
from scope_memory.paired_pilot import build,inference_input
class PilotTests(unittest.TestCase):
 def test_pairs_and_holdout(self):
  items=build()
  self.assertEqual(len(items),6)
  for f in {x["family"] for x in items}:
   group=[x for x in items if x["family"]==f]
   self.assertEqual(len({x["split"] for x in group}),1)
   self.assertEqual({x["kind"] for x in group},{"exception","update"})
 def test_no_labels(self):
  for x in build():
   self.assertTrue(all(set(t)=={"role","content"} for t in inference_input(x)))
 def test_gold_transition(self):
  for x in build():
   self.assertEqual(bool(x["gold"]["scopes"]),x["kind"]=="exception")
if __name__=="__main__":unittest.main()
