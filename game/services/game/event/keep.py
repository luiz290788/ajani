from google.appengine.ext import ndb

from services.game import response_util
from services.game import state
from services.model import Hand, Library, BattleField, Graveyard, Exile


def _gen_to_put(game, player_id):
  objs = []
  objs.append(BattleField(parent=game.key, id=player_id, cards=[]))
  objs.append(Graveyard(parent=game.key, id=player_id, cards=[]))
  objs.append(Exile(parent=game.key, id=player_id, cards=[]))
  objs.append(game)
  return objs

def _set_ready(game, player_id):
  if game.player_0 == player_id:
    game.ready_player_0 = True
  elif game.player_1 == player_id:
    game.ready_player_1 = True
  
  return game.ready_player_0 and game.ready_player_1

def load(incoming_event, player_id, game_key):
  hand_key = ndb.Key(Hand, player_id, parent=game_key)
  library_key = ndb.Key(Library, player_id, parent=game_key)
  return [hand_key, library_key]

def process(incoming_event, player_id, game, hand_obj, library_obj):
  
  if _set_ready(game, player_id):
    game.state = state.IN_GAME
    response_state = game.state
  else:
    response_state = state.WAIT_OPPONENT
  
  to_put = _gen_to_put(game, player_id)
  
  hand_response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  library_response = response_util.library_response(library_obj)
  empty_response = {'cards': []}
  
  response = {'state': response_state, 'hand': hand_response, 'library': library_response,
              'battlefield': empty_response, 'graveyard': empty_response, 'exile': empty_response}
  notification = {'state': response_state, 'opponent_library': library_response,
                  'opponent_hand': {'cards': len(hand_obj.cards)}, 'opponent_battlefield': empty_response,
                  'opponent_graveyard': empty_response, 'opponent_exile': empty_response}

  return (response, notification, to_put)
