from participant import Participant
from tournament_round import TournamentMatch, TournamentRound
from tournament import Tournament

from google.appengine.ext import ndb

class User(ndb.Model):
  gPlusId = ndb.StringProperty(required=True)
  tournaments_subscribed = ndb.StringProperty(repeated=True)

class MagicCard(ndb.Model):
  multiverse_id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  color = ndb.StringProperty(repeated=True)
  set = ndb.StringProperty(required=True)
  rarity = ndb.StringProperty(required=True)

class DeckCard(ndb.Model):
  multiverse_id = ndb.StringProperty(required=True)
  card_name = ndb.StringProperty(required=True)
  quantity = ndb.IntegerProperty(required=True)

class MagicDeck(ndb.Model):
  # parent = user.key()
  name = ndb.StringProperty(required=True)
  total_cards = ndb.IntegerProperty(required=True)
  swamp = ndb.IntegerProperty()
  island = ndb.IntegerProperty()
  plains = ndb.IntegerProperty()
  forrest = ndb.IntegerProperty()
  mountain = ndb.IntegerProperty()
  cards = ndb.StructuredProperty(DeckCard, repeated=True)
