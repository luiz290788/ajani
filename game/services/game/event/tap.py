from google.appengine.ext import ndb
from services.model import BattleField

def _get_response(bf):
  bf_response = {'cards': [card.to_dict() for card in bf.cards]}
  
  response = {'battlefield': bf_response}
  notification = {'opponent_battlefield': bf_response}
  
  return (response, notification)

def _set_tapped(game, player_id, card, tapped):
  bf = ndb.Key(BattleField, player_id, parent=game.key).get()
  card = bf.get_card(card)
  card.tapped = tapped
  bf.put()
  return _get_response(bf)

def tap_process(game, player_id, incoming_event):
  return _set_tapped(game, player_id, incoming_event['card'], True)
  
def untap_process(game, player_id, incoming_event):
  return _set_tapped(game, player_id, incoming_event['card'], False)

def untap_all_process(game, player_id, incoming_event):
  bf = ndb.Key(BattleField, player_id, parent=game.key).get()
  for card in bf.cards:
    card.tapped = False
    
  bf.put()

  return _get_response(bf)