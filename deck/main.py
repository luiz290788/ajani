import logging, json
from flask import Flask
from flask import request
from services.model import Deck
from services import deck

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
app = Flask(__name__)

@app.route('/deck', methods=['PUT'])
def create_deck():
  log.debug(request.get_json())
  deck_obj = Deck.from_dict(request.get_json())
  deck_obj = deck.create(deck_obj);

  return json.dumps(deck_obj.to_dict())

@app.route('/deck/<int:deck_id>', methods=['POST'])
def update_deck(deck_id):
  log.debug(request.get_json())
  deck_obj = Deck.from_dict(request.get_json())
  deck_obj = deck.update(deck_id, deck_obj)
  
  return json.dumps(deck_obj.to_dict())

@app.route('/deck/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
  log.info('loading deck: %d' % deck_id)
  deck_obj = deck.get(deck_id)
  return json.dumps(deck_obj.to_dict())

@app.route('/deck/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
  log.info('deleting deck: %d' % deck_id)
  deck.delete(deck_id)
  return ('', 204)