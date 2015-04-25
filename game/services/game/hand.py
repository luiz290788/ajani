from google.appengine.ext import ndb
from services.model import Hand

def get(game_urlsafe, player_id):
  game_key = ndb.Key(urlsafe=game_urlsafe)
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  hand = hand_key.get()
  if hand is None:
    game = game_key.get()
    hand = generate(game, player_id)   
  return hand

def generate(game, player_id):
  if game.player_0 == player_id:
    deck_id = game.deck_player_0
  elif game.player_1 == player_id:
    deck_id = game.deck_player_1
  
  deckservices.get(deck_id)