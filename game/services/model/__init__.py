from google.appengine.ext import ndb

class Game(ndb.Model):
  deck_player_0 = ndb.IntegerProperty()
  deck_player_1 = ndb.IntegerProperty()
