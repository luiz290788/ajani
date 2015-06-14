from google.appengine.ext import ndb

from services.game import library
from services.model import Hand, Library


def load(incoming_event, player_id, game_key):
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  library_key = ndb.Key(Library, player_id, parent=game_key)
  return [hand_key, library_key]

def process(incoming_event, player_id, game, hand_obj, library_obj):
  current_size = len(hand_obj.cards)
  
  library_obj.cards.extend(hand_obj.cards)  
  library.shuffle(library_obj)
  hand_obj.cards = []

  library.draw(library_obj, hand_obj, current_size - 1)
  
  response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  notification = None
  
  return (response, notification, [hand_obj, library_obj])