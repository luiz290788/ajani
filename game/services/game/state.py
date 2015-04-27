from google.appengine.ext import ndb
from services.model import Hand, Library

# waiting for the opponent
WAIT_OPPONENT = 'wait_opponent'

# when the users are selecting the deck
SELECT_DECK = 'select_deck'

# when the users are shuffling the decks and throwing dices
PRE_GAME = 'pre_game'

# when the game has started
IN_GAME = 'in_game'

# users are throwing dices to decide who starts
THROW_DICE = 'throw_dice'

# players are deciding if keep your mulligan
OPENING_HAND = 'opening_hand'

def _load_game_entities(game, player_id):
  keys = []
  keys.append(ndb.Key(Hand, game.player_0, parent=game.key))
  keys.append(ndb.Key(Hand, game.player_1, parent=game.key))
  keys.append(ndb.Key(Library, game.player_0, parent=game.key))
  keys.append(ndb.Key(Library, game.player_1, parent=game.key))
  
  response = {}
  objs = ndb.get_multi(keys)
  for obj in objs:
    if type(obj) is Hand:
      if obj.key.id() == player_id:
        response['hand'] = {'cards': [card.to_dict() for card in obj.cards]}
      else:
        response['opponent_hand'] = {'cards': len(obj.cards)}
    elif type(obj) is Library:
      library_response = {'cards': len(obj.cards)}
      if obj.key.id() == player_id:
        response['library'] = library_response
      else:
        response['opponent_library'] = library_response
  return response

def get(game, player_id):
  response = {}
  if game.state == SELECT_DECK:
    response['state'] = game.state
    if game.player_0 == player_id and game.deck_player_0 is not None \
        or game.player_1 == player_id and game.deck_player_1 is not None:
      response['state'] = WAIT_OPPONENT
  elif game.state == THROW_DICE:
    response['state'] = game.state
    if game.player_0 == player_id and game.deck_player_0 is not None \
        or game.player_1 == player_id and game.deck_player_1 is not None:
      response['state'] = WAIT_OPPONENT
  elif game.state == OPENING_HAND:
    response['state'] = game.state
  elif game.state == IN_GAME:
    response = _load_game_entities(game, player_id)
    response['state'] = game.state

  return response
