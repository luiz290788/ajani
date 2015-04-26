from google.appengine.ext import ndb
from services.model import Hand
from services.game import library

def get(game_urlsafe, player_id):
  game_key = ndb.Key(urlsafe=game_urlsafe)
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  hand = hand_key.get()
  if hand is None:
    game = game_key.get()
    hand = generate(game, player_id)   
  return hand

def generate(game, player_id):
  library_obj = library.get(game, player_id)
  hand_obj = Hand(parent=game.key, id=player_id, cards=[])
  return library.draw(library_obj, hand_obj, 7)