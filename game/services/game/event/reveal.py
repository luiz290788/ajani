from google.appengine.ext import ndb

from services.game import response_util
from services.model import Hand, Library


def reveal_hand_process(game, player_id, incoming_event):
  hand_obj = ndb.Key(Hand, player_id, parent=game.key).get()

  cards = {'cards': [card.to_dict() for card in hand_obj.cards]}
  response = {'reveal_hand': True}
  notification = {'opponent_revealed_hand': cards}

  return (response, notification)

def top_reveal_process(game, player_id, incoming_event):
  lb = ndb.Key(Library, player_id, parent=game.key).get()
  lb.top_revealed = incoming_event['top_revealed']
  lb.put()

  library_response = response_util.library_response(lb)
  response = {'library': library_response}
  notification = {'opponent_library': library_response}
  
  return (response, notification)

def reveal_card_process(game, player_id, incoming_event):
  h = ndb.Key(Hand, player_id, parent=game.key).get()
  card = h.get_card(incoming_event['card'])

  response = {'revel_card': True}
  notification = {'opponent_revealed_card': card.to_dict()}

  return (response, notification)