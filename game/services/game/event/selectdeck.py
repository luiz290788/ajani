from services.game import playerstate

def select_deck_process(game, player_id, incoming_event):
  deck = incoming_event['deck']
  if player_id == game.player_0 :
    game.deck_player_0 = deck
  elif player_id == game.player_1 :
    game.deck_player_1 = deck
  game.put()
  
  return {'state': playerstate.WAIT_OPPNENT}
