import logging, json
from flask import Flask
from services import game

log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/api/game/<kind>', methods=['PUT'])
def create(kind):
  game_obj = game.create(kind)
  response = {'game_id': game_obj.key.urlsafe()}
  return json.dumps(response)