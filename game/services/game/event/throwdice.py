from services.game import dice
from services.game.state import OPENING_HAND

def throw_dice_process(game, player_id, incoming_event):
  value = dice.throw(20)

  if game.player_0 == player_id:
    game.dice_player_0 = value
  else:
    game.dice_player_1 = value

  if game.dice_player_0 is not None and game.dice_player_1 is not None:
    game.state = OPENING_HAND
    
  game.put()

  response = {'dice_value': value, 'state': game.state}

  return (response, response)