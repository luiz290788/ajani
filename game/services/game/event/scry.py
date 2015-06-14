from google.appengine.ext import ndb

from services.game import response_util
from services.model import Library


def _get_cards(lb, card_ids):
  cards = []
  for card_id in card_ids:
    card = lb.get_card(card_id)
    lb.cards.remove(card)
    cards.append(card)
  return cards

def load(incoming_event, player_id, game_key):
  return [ndb.Key(Library, player_id, parent=game_key)]

def process(incoming_event, player_id, game, lb):
  
  response = None
  notification = None
  if 'count' in incoming_event:
    # requesting cards
    count = int(incoming_event['count'])
    scry_cards = lb.cards[0:count]
    response = {'scry': {'cards': [card.to_dict() for card in scry_cards]}}
    notification = {'toast': 'Opponent is scrying %d cards' % count}
    to_put = None
  elif 'top_cards' in incoming_event and 'bottom_cards' in incoming_event:
    # positioning cards
    top_cards = _get_cards(lb, incoming_event['top_cards'])
    bottom_cards = _get_cards(lb, incoming_event['bottom_cards'])
    lb.cards = top_cards + lb.cards + bottom_cards
    library_response = response_util.library_response(lb)
    response = {'scry': True, 'library': library_response}
    notification = {'opponent_library': library_response}
    to_put = [lb] 
  
  return (response, notification, to_put)
