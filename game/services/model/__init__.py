from google.appengine.ext import ndb

class Game(ndb.Model):
  kind = ndb.StringProperty()

  player_0 = ndb.StringProperty()
  player_1 = ndb.StringProperty()
  token_player_0 = ndb.StringProperty()
  token_player_1 = ndb.StringProperty()
  deck_player_0 = ndb.IntegerProperty()
  deck_player_1 = ndb.IntegerProperty()
  dice_player_0 = ndb.IntegerProperty()
  dice_player_1 = ndb.IntegerProperty()
  
  created_at = ndb.DateTimeProperty()
  state = ndb.StringProperty()

  @classmethod
  def from_urlsafe(cls, urlsafe):
    return ndb.Key(urlsafe=urlsafe).get()
  
class Event(ndb.Model):
  data = ndb.JsonProperty(compressed=True)
  player_id = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)
  