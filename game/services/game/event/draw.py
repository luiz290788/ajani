from google.appengine.ext import ndb

from services.game import library, response_util
from services.model import Hand, Library

def load(incoming_event, player_id, game_key):
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  library_key = ndb.Key(Library, player_id, parent=game_key)
  return [hand_key, library_key]
  

def process(incoming_event, player_id, game, hand_obj, library_obj):
  count = incoming_event['count'] if incoming_event['count'] is not None else 0
  
  hand_obj = library.draw(library_obj, hand_obj, count)

  to_put = [hand_obj, library_obj]
  
  hand_response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  library_response = response_util.library_response(library_obj)
  
  response = {'hand': hand_response, 'library': library_response}
  notification = {'opponent_hand': {'cards': len(hand_obj.cards)},
                  'opponent_library': library_response}
  
  return (response, notification, to_put)
  