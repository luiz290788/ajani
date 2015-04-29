from google.appengine.ext import ndb
from services.game import response_util
from services.model import Hand, Library, BattleField, Graveyard, Exile

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

def _get_key(game, entity):
  keys = []
  keys.append(ndb.Key(entity, game.player_0, parent=game.key))
  keys.append(ndb.Key(entity, game.player_1, parent=game.key))
  return keys

def _load_game_entities(game, player_id):
  keys = []
  keys.extend(_get_key(game, Hand))
  keys.extend(_get_key(game, Library))
  keys.extend(_get_key(game, BattleField))
  keys.extend(_get_key(game, Graveyard))
  keys.extend(_get_key(game, Exile))
  
  response = {}
  objs = ndb.get_multi(keys)
  for obj in objs:
    if type(obj) is Hand:
      if obj.key.id() == player_id:
        response['hand'] = {'cards': [card.to_dict() for card in obj.cards]}
      else:
        response['opponent_hand'] = {'cards': len(obj.cards)}
    elif type(obj) is Library:
      library_response = response_util.library_response(obj)
      if obj.key.id() == player_id:
        response['library'] = library_response
      else:
        response['opponent_library'] = library_response
    elif type(obj) is BattleField:
      battlefield_response = {'cards': [card.to_dict() for card in obj.cards]}
      if obj.key.id() == player_id:
        response['battlefield'] = battlefield_response
      else:
        response['opponent_battlefield'] = battlefield_response
    elif type(obj) is Graveyard:
      graveyard_response = {'cards': [card.to_dict() for card in obj.cards]}
      if obj.key.id() == player_id:
        response['graveyard'] = graveyard_response
      else:
        response['opponent_graveyard'] = graveyard_response
    elif type(obj) is Exile:
      exile_response = {'cards': [card.to_dict() for card in obj.cards]}
      if obj.key.id() == player_id:
        response['exile'] = exile_response
      else:
        response['opponent_exile'] = exile_response
    
  return response


def _set_life(game, player_id, response):
  if game.player_0 == player_id:
    response['life'] = game.life_player_0
    response['opponent_life'] = game.life_player_1
  elif game.player_1 == player_id:
    response['life'] = game.life_player_1
    response['opponent_life'] = game.life_player_0

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
    _set_life(game, player_id, response)

  return response
