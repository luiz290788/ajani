from google.appengine.ext import ndb
from services.game import state
from services.model import Hand, Library, BattleField, Graveyard, Exile

def _gen_objs(game, player_id):
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
  
  objs = _gen_objs(game, player_id)
  ndb.put_multi(objs)
  
  hand_response = {'cards': [card.to_dict() for card in hand.cards]}
  library_response = {'cards': len(library.cards)}
  empty_response = {'cards': []}
  
  response = {'state': response_state, 'hand': hand_response, 'library': library_response,
              'battlefield': empty_response, 'graveyard': empty_response, 'exile': empty_response}
  notification = {'state': response_state, 'opponent_library': library_response,
                  'opponent_hand': {'cards': len(hand.cards)}, 'opponent_battlefield': empty_response,
                  'opponent_graveyard': empty_response, 'opponent_exile': empty_response}

  return (response, notification)
