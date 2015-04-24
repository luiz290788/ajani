from services.game import dice
from services.game.state import OPENING_HAND

def _is_player_0(game, player_id):
  return game.player_0 == player_id

def throw_dice_process(game, player_id, incoming_event):
  player_0 = _is_player_0(game, player_id)

  throw_dice = False
  if player_0 and game.dice_player_0 is None or \
      not player_0 and game.dice_player_1 is None:
    throw_dice = True
  
  if throw_dice:
    value = dice.throw(20)
    if player_0:
      game.dice_player_0 = value
    else:
      game.dice_player_1 = value

    if game.dice_player_0 is not None and game.dice_player_1 is not None:
      if game.dice_player_0 != game.dice_player_1:
        game.state = OPENING_HAND
      else:
        game.dice_player_0 = None
        game.dice_player_1 = None
  elif player_0:
    value = game.dice_player_0
  else:
    value = game.dice_player_1
    
  game.put()

  response = {'dice_value': value, 'state': game.state}

  return (response, response)