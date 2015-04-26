import logging, json
from flask import Flask, request
from services import game
from services.game import dice, state, hand
from google.appengine.api import channel
from services.model import Game

log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/api/game/<kind>', methods=['PUT'])
def create(kind):
  game_obj = game.create(kind)
  response = {'game_id': game_obj.key.urlsafe()}
  return json.dumps(response)

@app.route('/api/game/<game_id>', methods=['POST'])
def connect(game_id):
  (token, player_id) = game.connect(game_id)
  token = channel.create_channel(token)
  response = {'game_id': game_id, 'token': token, 'player': player_id}
  return json.dumps(response)

@app.route('/api/game/<game_id>/<player_id>', methods=['GET'])
def get_state(game_id, player_id):
  game_obj = Game.from_urlsafe(game_id)
  response = state.get(game_obj, player_id)
  return json.dumps(response)

@app.route('/api/game/<game_id>/<player_id>', methods=['PUT'])
def event(game_id, player_id):
  event = request.get_json()
  game_obj = Game.from_urlsafe(game_id)
  state = game.process_event(game_obj, player_id, event)
  return json.dumps(state)

@app.route('/api/game/<game_id>/<player_id>/hand', methods=['GET'])
def get_hand(game_id, player_id):
  hand_obj = hand.get(game_id, player_id)
  response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  return json.dumps(response)
  
@app.route('/api/game/dice/<int:dice_size>', methods=['GET'])
def throw_dice(dice_size):
  result = dice.throw(dice_size)
  response = {'size' : dice_size, 'result': result}
  return json.dumps(response)
