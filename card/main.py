import logging, json
from flask import Flask
from flask import request
from services import card
from services.card import importer, search

log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/import/all', methods=['POST'])
def import_all():
  log.info('importing all sets...')
  importer.import_all()
  return 'importing all sets'

@app.route('/import/set/<card_set>', methods=['POST'])
def import_set(card_set):
  log.info('importing set %s' % card_set)
  importer.import_set(card_set)
  return 'importing set'

@app.route('/card', methods=['GET'])
def search_cards():
  result = {}
  if 'q' in request.args:
    term = request.args['q']
    result['term'] = term 
    result['cards'] = search.do_search(term)
  return json.dumps(result)

@app.route('/card/<int:multiverseid>', methods=['GET'])
def get_card(multiverseid):
  magic_card = card.get_card(multiverseid)
  card_dict = magic_card.to_dict()
  card_dict['multiverseid'] = multiverseid
  return json.dumps(card_dict)
