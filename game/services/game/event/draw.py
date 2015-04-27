from google.appengine.ext import ndb
from services.model import Hand, Library
from services.game import library

def draw_process(game, player_id, incoming_event):
  hand_key = ndb.Key(Hand, player_id, parent=game.key)
  library_key = ndb.Key(Library, player_id, parent=game.key)
  [hand_obj, library_obj] = ndb.get_multi([hand_key, library_key])
  
  count = 1
  if incoming_event['count'] is not None:
    count = incoming_event['count']
  
  hand_obj = library.draw(library_obj, hand_obj, count)
  
  hand_response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  library_response = {'cards': len(library_obj.cards)}
  
  response = {'hand': hand_response, 'library': library_response}
  notification = {'opponent_hand': {'cards': len(hand_obj.cards)},
                  'opponent_library': library_response}
  
  return (response, notification)
  