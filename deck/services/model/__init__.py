import logging
from google.appengine.ext import ndb
from google.appengine.api import search

log = logging.getLogger(__name__)

class Card(ndb.Model):
  quantity = ndb.IntegerProperty(required=True)
  multiverse_id = ndb.StringProperty(required=True)

class Deck(ndb.Model):
  INDEX = 'deck'
  
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty()
  cards = ndb.StructuredProperty(Card, repeated=True)
  
  @classmethod
  def from_dict(cls, deck_dict):
    deck = Deck()

    deck.name = deck_dict['name']
    if 'description' in deck_dict :
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
  
    
  def _post_put_hook(self, future):
    log.info('adding %s deck to deck index' % self.name)
    ndb.Model._post_put_hook(self, future)
    index = search.Index(self.INDEX)
    document = search.Document(doc_id=str(self.key.id()),
      fields=[search.TextField(name='name', value=self.name)])
    index.put(document)
    
  @classmethod
  def _post_delete_hook(cls, key, future):
    super(Deck, cls)._post_delete_hook(key, future)
    deck_id = str(key.id())
    index = search.Index(cls.INDEX)
    index.delete([deck_id])
