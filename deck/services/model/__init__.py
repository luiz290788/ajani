import logging
from google.appengine.ext import ndb

log = logging.getLogger(__name__)

class Card(ndb.Model):
  quantity = ndb.IntegerProperty(required=True)
  multiverse_id = ndb.StringProperty(required=True)

class Deck(ndb.Model):
  
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty()
  cards = ndb.StructuredProperty(Card, repeated=True)
  
  @classmethod
  def from_dict(cls, deck_dict):
    deck = Deck()

    deck.name = deck_dict['name']
    deck.description = deck_dict['description']
    deck.cards = []
    log.debug(deck_dict['cards'])
    for multiverse_id, quantity in deck_dict['cards'].iteritems():
      deck.cards.append(Card(multiverse_id = multiverse_id,
                             quantity = quantity))
    
    return deck
  
  def to_dict(self, include=None, exclude=None):
    deck_dict = ndb.Model.to_dict(self, include=include, exclude=exclude)
    deck_dict['id'] = self.key.id()
    return deck_dict
