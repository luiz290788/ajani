from google.appengine.ext import ndb

class Game(ndb.Model):
  kind = ndb.StringProperty()
  token_player_0 = ndb.StringProperty()
  token_player_1 = ndb.StringProperty()
  deck_player_0 = ndb.IntegerProperty()
  deck_player_1 = ndb.IntegerProperty()
  created_at = ndb.DateTimeProperty()
