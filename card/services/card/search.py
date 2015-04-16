from google.appengine.api import search
from services.card import CARD_INDEX_NAME

SEARCH_LIMIT = 10

def do_search(term):
  options = search.QueryOptions(limit=SEARCH_LIMIT, returned_fields=['card_name'])
  query = search.Query('name_tokens: %s' % term, options)
  index = search.Index(name=CARD_INDEX_NAME)
  results = index.search(query)

  cards = []

  for result in results.results:
      card = {'multiverse_id': result.doc_id}
      for field in result.fields:
        if field.name == 'card_name':
          card['card_name'] = field.value
      cards.append(card)
      
  return cards