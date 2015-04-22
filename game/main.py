import logging, json
from flask import Flask
from services import game
from google.appengine.api import channel

log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/api/game/<kind>', methods=['PUT'])
def create(kind):
  game_obj = game.create(kind)
  response = {'game_id': game_obj.key.urlsafe()}
  return json.dumps(response)

@app.route('/api/game/<game_id>', methods=['POST'])
def connect(game_id):
  token = game.connect(game_id)
  token = channel.create_channel(token)
  response = {'game_id': game_id, 'token': token}
  return json.dumps(response)