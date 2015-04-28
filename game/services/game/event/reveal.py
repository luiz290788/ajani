from google.appengine.ext import ndb
from services.model import Hand


def reveal_hand_process(game, player_id, incoming_event):
  hand_obj = ndb.Key(Hand, player_id, parent=game.key).get()

  cards = {'cards': [card.to_dict() for card in hand_obj.cards]}
  response = {'reveal_hand': True}
  notification = {'opponent_revealed_hand': cards}

  return (response, notification)