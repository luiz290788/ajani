import logging
from google.appengine.ext import ndb
from services.model import Deck
from google.appengine.api.search.search import SortExpression, Index, QueryOptions,\
  SortOptions, Query

log = logging.getLogger(__name__)

def create(deck):
  deck.put()
  return deck

def get(deck_id):
  key = ndb.Key(Deck, deck_id)
  return key.get()

def update(deck_id, deck_obj):
  key = ndb.Key(Deck, deck_id)
  deck_obj.key = key
  deck_obj.put()
  return deck_obj

def delete(deck_id):
  key = ndb.Key(Deck, deck_id)
  key.delete()

def list_deck():
  index = Index(Deck.INDEX)
  name_sort = SortExpression(expression='name', direction=SortExpression.ASCENDING, default_value='')
  sort_options = SortOptions(expressions=[name_sort])
  options = QueryOptions(returned_fields=['name'], sort_options=sort_options)
  query = Query(query_string='', options=options)
  
  results = index.search(query)
  
  decks = []
  for result in results.results:
    deck = {'id': result.doc_id}
    for field in result.fields:
      if field.name == 'name':
        deck['name'] = field.value
    decks.append(deck)
  
  return decks
