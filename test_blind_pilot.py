import json,unittest
from pathlib import Path
from score_blind_pilot import score
P=Path(__file__).parent
class BlindPilotTests(unittest.TestCase):
 def test_input_is_blind(self):
  x=json.loads((P/"blind_packet.json").read_text())
  self.assertEqual(len(x["items"]),12)
  for item in x["items"]:
   self.assertEqual(set(item),{"id","messages"})
   for m in item["messages"]:self.assertEqual(set(m),{"role","content"})
 def test_family_split(self):
  g=json.loads((P/"blind_gold.json").read_text())
  for fam in {v["family"] for v in g.values()}:
   group=[v for v in g.values() if v["family"]==fam]
   self.assertEqual(len({v["split"] for v in group}),1)
   self.assertEqual({v["label"] for v in group},{"scoped_exception","lasting_update","insufficient"})
 def test_locked_results(self):
  r=score(json.loads((P/"blind_gold.json").read_text()),json.loads((P/"blind_locked_labels.json").read_text()))
  self.assertEqual(r["agreement"],12);self.assertEqual(r["disagreements"],[])
if __name__=="__main__":unittest.main()
