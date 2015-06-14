from google.appengine.ext import ndb

from services.game import response_util
from services.model import Hand, Library

def hand_load(incoming_event, player_id, game_key):
  return [ndb.Key(Hand, player_id, parent=game_key)]


def hand_process(incoming_event, player_id, game, hand_obj):
  cards = {'cards': [card.to_dict() for card in hand_obj.cards]}
  response = {'reveal_hand': True}
  notification = {'opponent_revealed_hand': cards}

  return (response, notification, None)

def top_load(incoming_event, player_id, game_key):
  return [ndb.Key(Library, player_id, parent=game_key)]

def top_process(incoming_event, player_id, game, lb):
  lb.top_revealed = incoming_event['top_revealed']

  library_response = response_util.library_response(lb)
  response = {'library': library_response}
  notification = {'opponent_library': library_response}
  
  return (response, notification, [lb])

def card_load(incoming_event, player_id, game_key):
  return [ndb.Key(Hand, player_id, parent=game_key)]

def card_process(incoming_event, player_id, game, h):
  card = h.get_card(incoming_event['card'])

  response = {'revel_card': True}
  notification = {'opponent_revealed_card': card.to_dict()}

  return (response, notification, None)

def top_cards_load(incoming_event, player_id, game_key):
  return [ndb.Key(Library, player_id, parent=game_key)]

def reveal_top_cards(incoming_event, player_id, game, lb):
  count = incoming_event.get('count', 1)
  cards = lb.cards[0:count]
  cards_response = {'cards': [response_util.card_response(card) for card in cards]}
  response = {'cards_revealed': cards_response}
  notification = {'opponent_cards_revealed': cards_response}
  return (response, notification, None)