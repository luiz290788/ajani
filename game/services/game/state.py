
# waiting for the opponent
WAIT_OPPONENT = 'wait_opponent'

# when the users are selecting the deck
SELECT_DECK = 'select_deck'

# when the users are shuffling the decks and throwing dices
PRE_GAME = 'pre_game'

# when the game has started
IN_GAME = 'in_game'

# users are throwing dices to decide who starts
THROW_DICES = 'throw_dices'

def get(game, player_id):
  response = {}
  if game.state == SELECT_DECK:
    response['state'] = game.state
    if game.player_0 == player_id and game.deck_player_0 is not None \
        or game.player_1 == player_id and game.deck_player_1 is not None:
      response['state'] = WAIT_OPPONENT
      
  return response