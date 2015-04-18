import logging, json
from flask import Flask
from flask import request
from services.model import Deck
from services import deck

log = logging.getLogger(__name__)
app = Flask(__name__)

def _deck_response(deck_obj):
  deck_dict = deck_obj.to_dict()
  deck_dict['id'] = deck_obj.key.id()
  cards = deck_dict['cards']
  deck_dict['cards'] = {}
  
  for card in cards:
    deck_dict['cards'][card['multiverse_id']] = card['quantity']
  
  return deck_dict

@app.route('/api/deck', methods=['PUT'])
def create_deck():
  log.debug(request.get_json())
  deck_obj = Deck.from_dict(request.get_json())
  deck_obj = deck.create(deck_obj);

  return json.dumps(_deck_response(deck_obj))

@app.route('/api/deck/<int:deck_id>', methods=['POST'])
def update_deck(deck_id):
  log.debug(request.get_json())
  deck_obj = Deck.from_dict(request.get_json())
  deck_obj = deck.update(deck_id, deck_obj)
  
  return json.dumps(_deck_response(deck_obj))

@app.route('/api/deck/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
  log.info('loading deck: %d' % deck_id)
  deck_obj = deck.get(deck_id)

  return json.dumps(_deck_response(deck_obj))

@app.route('/api/deck/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
  log.info('deleting deck: %d' % deck_id)
  deck.delete(deck_id)
  return ('', 204)