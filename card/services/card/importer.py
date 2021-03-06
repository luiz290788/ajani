import json
from google.appengine.api import urlfetch, search, taskqueue
from services.model import MagicCard
from services.card import CARD_INDEX_NAME
from services.util import _tokenize_string, _save_batch

MTG_JSON_URL = 'http://mtgjson.com/json/SetCodes.json'
MTG_JSON_CARD_SET_URL = 'http://mtgjson.com/json/%s.json'

SET_IMPORTER_QUEUE = 'SetImporter'
IMPORTER_TASK_URL = '/import/set/%s'

def import_all():
  url = MTG_JSON_URL
  sets_list = json.loads(urlfetch.fetch(url).content)
  queue = taskqueue.Queue(SET_IMPORTER_QUEUE)
  tasks = []
  for card_set in sets_list:
    task = taskqueue.Task(url=IMPORTER_TASK_URL % card_set, method='POST')
    tasks.append(task)
    if len(tasks) == 100:
      queue.add(tasks)
      tasks = []
  queue.add(tasks)

def _search_document(json_card):
  card_document = search.Document(
    doc_id=str(json_card['multiverseid']),
    fields=[
      search.TextField(
        name='card_name',
        value=json_card['name']),
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
