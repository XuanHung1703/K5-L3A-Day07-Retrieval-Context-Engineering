import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'solution'))
from lab7 import Retrieval,pack_context
class PipelineTests(unittest.TestCase):
 def setUp(self):
  self.chunks=[{'id':'a','text':'alpha beta','source_id':'s','source':'s','page':1,'metadata':{}},{'id':'b','text':'gamma delta','source_id':'s','source':'s','page':2,'metadata':{}}]
 def test_lexical_query(self):
  self.assertEqual(Retrieval(self.chunks,'tfidf').search('gamma')[0]['id'],'b')
 def test_invalid_method(self):
  with self.assertRaises(ValueError):Retrieval(self.chunks,'fake')
 def test_hybrid_merges_ids(self):
  r=Retrieval(self.chunks,'hybrid');r.dense=lambda q,k:[dict(self.chunks[0],score=.9),dict(self.chunks[1],score=.8)]
  results=r.search('gamma');self.assertEqual(len({c['id'] for c in results}),len(results));self.assertEqual(results[0]['id'],'b')
 def test_context_budget(self):
  context,ids=pack_context(self.chunks,1);self.assertEqual(context,'');self.assertEqual(ids,[])
