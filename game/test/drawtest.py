import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class Test(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_modules_stub()
    
    ndb.get_context().clear_cache()
    

  def testLoad(self):
    from services import game
    game_obj = game.create('standard')
    (_, player_0) = game.connect(game_obj.key)
    (_, _) = game.connect(game_obj.key)

    game.process_event(game_obj.key, player_0, {'count': 1, 'event': 'draw'})


if __name__ == "__main__":
  unittest.main()