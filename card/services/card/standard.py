from services.card.importer import MTG_JSON_CARD_SET_URL, SET_IMPORTER_QUEUE
from services.card.search import SEARCH_LIMIT
from google.appengine.api import taskqueue, urlfetch, search
import json
from services.model import MagicCard
from services.util import _tokenize_string, _save_batch

STANDARD_SETS = ['THS', 'BNG', 'JOU', 'M15', 'KTK', 'FRF', 'DTK']

IMPORTER_TASK_URL = '/import/standard/%s'
CARD_INDEX_NAME = 'standard'

def clear_index():
  pass

def build_index():
  clear_index()
  queue = taskqueue.Queue(SET_IMPORTER_QUEUE)
  for card_set in STANDARD_SETS:
    task = taskqueue.Task(url=IMPORTER_TASK_URL % card_set, method='POST')
    queue.add(task)
    

def _search_document(json_card):
  card_document = search.Document(
    doc_id=str(json_card['multiverseid']),
    fields=[
      search.TextField(
        name='card_name',
        value=json_card['name']),
      search.TextField(
        name='set',
        value=json_card['set']),
      search.TextField(
        name='name_tokens',
        value=' '.join(_tokenize_string(json_card['name'])))
    ]
  )
  return card_document

def import_set(card_set):
  url = MTG_JSON_CARD_SET_URL % card_set
  set_data = json.loads(urlfetch.fetch(url).content)
  index = search.Index(name=CARD_INDEX_NAME)
  
  cards = []
  documents = []
  for json_card in set_data['cards']:
    if 'multiverseid' in json_card:
      json_card['set'] = card_set
      cards.append(MagicCard.from_dict(json_card))
      documents.append(_search_document(json_card))
      if len(documents) >= 200:
        _save_batch(index, cards, documents)
        documents = []
        cards = []
  _save_batch(index, cards, documents)
  
def do_search(term):
  options = search.QueryOptions(limit=SEARCH_LIMIT, returned_fields=['card_name', 'set'])
  query = search.Query('name_tokens: %s' % term, options)
  index = search.Index(name=CARD_INDEX_NAME)
  results = index.search(query)

  cards = []

  for result in results.results:
      card = {'multiverse_id': result.doc_id}
      for field in result.fields:
        if field.name == 'card_name':
          card['card_name'] = field.value
        if field.name == 'set':
          card['set'] = field.value
      cards.append(card)
      
  return cards
  