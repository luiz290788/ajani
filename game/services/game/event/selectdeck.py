from services.game.state import THROW_DICES, WAIT_OPPONENT

def _set_deck(game, player_id, incoming_event):
  deck = incoming_event['deck']
  if player_id == game.player_0 :
    game.deck_player_0 = deck
  elif player_id == game.player_1 :
    game.deck_player_1 = deck


def _decks_selected(game):
  return game.deck_player_0 is not None and game.deck_player_1 is not None

def select_deck_process(game, player_id, incoming_event):
  _set_deck(game, player_id, incoming_event)
  
  response = {}
  notification = None
  if _decks_selected(game):
    game.state = THROW_DICES
    # TODO return current state to the user and notify the other user
    response['state'] = THROW_DICES
    notification = {'state': THROW_DICES}
  else:
    response['state'] = WAIT_OPPONENT
  game.put()

  return (response, notification)