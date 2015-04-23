import logging, json
from flask import Flask, request
from services import game
from services.game import dice
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
  state = game.get_state(game_id, player_id)
  
  return json.dumps(state)

@app.route('/api/game/<game_id>/<player_id>', methods=['PUT'])
def event(game_id, player_id):
  event = request.get_json()
  game_obj = Game.from_urlsafe(game_id)
  state = game.process_event(game_obj, player_id, event)
  return json.dumps(state)

@app.route('/api/game/dice/<int:dice_size>', methods=['GET'])
def throw_dice(dice_size):
  result = dice.throw(dice_size)
  response = {'size' : dice_size, 'result': result}
  return json.dumps(response)
