from google.appengine.ext import ndb
from services.model import BattleField

def _get_response(bf):
  bf_response = {'cards': [card.to_dict() for card in bf.cards]}
  
  response = {'battlefield': bf_response}
  notification = {'opponent_battlefield': bf_response}
  
  return (response, notification, [bf])

def _set_tapped(bf, card, tapped):
  card = bf.get_card(card)
  card.tapped = tapped
  return _get_response(bf)

def load(incoming_event, player_id, game_key):
  return [ndb.Key(BattleField, player_id, parent=game_key)]

def process(incoming_event, player_id, game, bf):
  return _set_tapped(bf, incoming_event['card'], True)
  
def untap_process(incoming_event, player_id, game, bf):
  return _set_tapped(bf, incoming_event['card'], False)

def untap_all_process(incoming_event, player_id, game, bf):
  for card in bf.cards:
    card.tapped = False
    
  return _get_response(bf)