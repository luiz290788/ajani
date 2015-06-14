from google.appengine.ext import ndb
from services.model import Hand
from services.game import library

def get(game_key, player_id):
  if type(game_key) is str or type(game_key) is unicode:
    game_key = ndb.Key(urlsafe=game_key)    
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  hand = hand_key.get()
  if hand is None:
    game = game_key.get()
    hand = generate(game, player_id)   
  return hand

def generate(game, player_id):
  library_obj = library.get(game, player_id)
  hand_obj = Hand(parent=game.key, id=player_id, cards=[])
  hand_obj = library.draw(library_obj, hand_obj, 7)
  ndb.put_multi([library_obj, hand_obj])
  return hand_obj