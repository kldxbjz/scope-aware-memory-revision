import unittest
from audit_horizon import visible_prefix,audit
class AuditTests(unittest.TestCase):
 def test_visible_only(self):
  c=[{"date":"1","conversation":{"turns":[{"role":"user","content":"hi","preference_expressed":{"gold":"secret"}}]}},{"date":"2","conversation":{"turns":[{"role":"user","content":"future"}]}}]
  self.assertEqual(visible_prefix(c,"1"),[{"date":"1","role":"user","content":"hi"}])
 def test_same_date_cutoff(self):
  c=[{"date":"1","conversation":{"turns":[{"role":"user","content":"seen"},{"role":"assistant","content":"future turn"}]}},{"date":"1","conversation":{"turns":[{"role":"user","content":"future conversation"}]}}]
  self.assertEqual([x["content"] for x in visible_prefix(c,"1",0,0)],["seen"])
 def test_reject_truncated(self):
  with self.assertRaises(ValueError): audit({"rows":[{"truncated_cells":["conversations"]}]})
 def test_dedupe_and_abstain(self):
  state={"evolution_history":[{"date":"2","attribute_changes":{"x":{"from":"a","to":"b"}}}]}
  r=audit({"rows":[{"row":{"user_id":"toy","generator":"fixture","preference_record":{"2":{"p":state},"3":{"p":state}},"conversations":[]}}]})
  self.assertEqual(r["users"][0]["unique_latent_change_records"],1)
  self.assertEqual(r["users"][0]["ambiguous_or_unverified"],1)
if __name__=="__main__": unittest.main()
