from services.model import Game
from google.appengine.ext import ndb
from datetime import datetime

def _generate_token(game_id, player_num):
  return '%d-%d' % (game_id, player_num)

def create(kind):
  (game_id, _) = Game.allocate_ids(size=1)
  game = Game(key=ndb.Key(Game, game_id), kind=kind,
        token_player_0=_generate_token(game_id, 0),
        token_player_1=_generate_token(game_id, 1),
        created_at=datetime.now())

  game.put()
  
  return game
  