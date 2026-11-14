import unittest
from read_write_diagnostic import *
class DiagnosticTests(unittest.TestCase):
 def test_read_overapply_not_overwrite(self):
  r=read_diagnostic(lambda p:reader(p,"overapply"))
  self.assertEqual(r["ordinary_side"]["errors"],3)
  self.assertEqual(r["scoped_side"]["errors"],0)
  self.assertEqual(r["writes_performed"],0)
  self.assertEqual(r["read_input_mutations"],0)
 def test_write_faults_distinct(self):
  self.assertEqual(write_diagnostic("persist_exception")["false_overwrite"]["errors"],3)
  self.assertEqual(write_diagnostic("persist_exception")["missed_durable_update"]["errors"],0)
  self.assertEqual(write_diagnostic("drop_update")["missed_durable_update"]["errors"],3)
  self.assertEqual(write_diagnostic("drop_update")["false_overwrite"]["errors"],0)
 def test_fixed_memory_request_and_no_gold(self):
  for ex,_,ctx,_ in families():
   a=read_input(ex["gold"],ex["family"],ctx);b=read_input(ex["gold"],ex["family"],"ordinary")
   self.assertEqual(a["memory"],b["memory"]);self.assertEqual(a["request"],b["request"])
   self.assertEqual(set(a),{"memory","request","situation"})
 def test_correct_and_denominators(self):
  self.assertEqual(read_diagnostic(reader)["both_sides_correct"],{"count":3,"denominator":3})
  self.assertEqual(write_diagnostic()["chronological_probe_errors"],metric(0,18))
 def test_mutating_reader_detected(self):
  def bad(p):
   p["memory"]["general"]="corrupt"
   return "wrong"
  self.assertEqual(read_diagnostic(bad)["read_input_mutations"],6)
if __name__=="__main__":unittest.main()
