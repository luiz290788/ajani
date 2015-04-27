from google.appengine.ext import ndb

class Game(ndb.Model):
  kind = ndb.StringProperty()

  player_0 = ndb.StringProperty()
  player_1 = ndb.StringProperty()
  ready_player_0 = ndb.BooleanProperty(default=False)
  ready_player_1 = ndb.BooleanProperty(default=False)
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

class Card(ndb.Model):
  multiverse_id = ndb.StringProperty(required=True)
  instance_id = ndb.IntegerProperty(required=True)

class CardHolder(ndb.Model):
  cards = ndb.StructuredProperty(Card, repeated=True)
  
  def get_card(self, instance_id):
    for card in self.cards:
      if card.instance_id == instance_id:
        return card
  
    return None

class Hand(CardHolder): pass

class Library(CardHolder): pass

class BattleField(CardHolder): pass

class Exile(CardHolder): pass

class Graveyard(CardHolder): pass
  