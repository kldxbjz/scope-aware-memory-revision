import unittest
from preflight import guard,parity,encode
class Toy:
 eos_token_id=999
 def __call__(self,s,**kw):return {'input_ids':[ord(x) for x in s],'offset_mapping':[(i,i+1) for i in range(len(s))]}
class Tests(unittest.TestCase):
 def test_prompt_parity_failure(self):
  with self.assertRaises(AssertionError):parity({'1':{'prompt':'a','split':'train'}},{'1':{'prompt':'b','split':'train'}})
 def test_too_short_rejected(self):
  with self.assertRaises(ValueError):guard([1,2],1)
 def test_mask_and_eos_algebra_only(self):
  f=encode({'prompt':'P','completion':'{}'},Toy(),10)
  self.assertEqual(f['labels'],[-100,-100,123,125,999])
if __name__=='__main__':unittest.main()
