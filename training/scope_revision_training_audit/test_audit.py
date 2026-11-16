import unittest
from audit import overlaps,cue_probe,txt
class Tests(unittest.TestCase):
 def test_normalized_collision_not_only_ids(self):
  a=[{'id':'a','prefix':[{'role':'user','text':'Use BLUE!'}]}];b=[{'id':'b','prefix':[{'role':'user','text':'use blue'}]}]
  r=overlaps(a,b);self.assertEqual(r['id'],[]);self.assertEqual(len(r['exact_normalized_full']),1)
 def test_nested_conversation(self):
  r={'input':{'memory':[{'text':'secret'}],'conversation':[{'role':'assistant','content':'question'},{'role':'user','content':'answer'}]}}
  self.assertEqual(txt(r,'last_user_only'),'answer');self.assertEqual(txt(r,'assistant_only'),'question')
 def test_template_exclusion(self):
  rr=[{'id':str(i),'family':str(i),'template_family':'shared','action':'no_op','prefix':[]} for i in range(2)]
  self.assertEqual(cue_probe(rr,'assistant_only')['no_disjoint_neighbor'],2)
 def test_balanced_identical_cue(self):
  rr=[{'id':str(i),'family':str(i),'action':a,'prefix':[{'role':'assistant','text':'one same sentence'}]} for i,a in enumerate(['a','b','a','b'])]
  self.assertEqual(cue_probe(rr,'assistant_only')['accuracy'],0.5)
if __name__=='__main__':unittest.main()
