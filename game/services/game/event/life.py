import re

def process(incoming_event, player_id, game):
  delta = incoming_event['delta']
  plus = None
  if type(delta) is unicode or type(delta) is str:
    m = re.search('^([+-]?)(\d+)$', delta)
    if m is not None:
      plus = m.group(1) == '+' or m.group(1) == ''
      delta = int(m.group(2))
  elif type(delta) is int or type(delta) is long:
    plus = True
    pass
  if plus is not None:
    if not plus:
      delta = -1 * delta
    if game.player_0 == player_id:
      game.life_player_0 = game.life_player_0 + delta
    else:
      game.life_player_1 = game.life_player_1 + delta
  
  if game.player_0 == player_id:
    life = game.life_player_0
  elif game.player_1 == player_id:
    life = game.life_player_1
  
  response = {'life': life}
  notification = {'opponent_life': life}
  
  return (response, notification, [game])