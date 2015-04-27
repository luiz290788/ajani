from google.appengine.ext import ndb
from services.game import state
from services.model import Hand, Library


def _set_ready(game, player_id):
  if game.player_0 == player_id:
    game.ready_player_0 = True
  elif game.player_1 == player_id:
    game.ready_player_1 = True
  
  return game.ready_player_0 and game.ready_player_1

def keep_process(game, player_id, incoming_event):
  hand_key = ndb.Key(Hand, player_id, parent=game.key)
  library_key = ndb.Key(Library, player_id, parent=game.key)
  result = ndb.get_multi([hand_key, library_key])
  hand = result[0]
  library = result[1]
  
  if _set_ready(game, player_id):
    game.state = state.IN_GAME
    response_state = game.state
  else:
    response_state = state.WAIT_OPPONENT
  
  game.put()
  
  hand_response = {'cards': [card.to_dict() for card in hand.cards]}
  library_response = {'cards': len(library.cards)}
  
  response = {'hand': hand_response, 'library': library_response, 'state': response_state}
  notification = {'opponent_library': library_response,
                  'opponent_hand': {'cards': len(hand.cards)}, 'state': response_state}

  return (response, notification)
