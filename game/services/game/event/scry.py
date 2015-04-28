from services.game import library

def _get_cards(lb, card_ids):
  cards = []
  for card_id in card_ids:
    card = lb.get_card(card_id)
    lb.cards.remove(card)
    cards.append(card)
  return cards

def scry_process(game, player_id, incoming_event):
  lb = library.get(game, player_id)
  
  response = None
  notification = None
  if 'count' in incoming_event:
    # requesting cards
    count = int(incoming_event['count'])
    scry_cards = lb.cards[0:count]
    response = {'scry': {'cards': [card.to_dict() for card in scry_cards]}}
    notification = {'toast': 'Opponent is scrying %d cards' % count}
  elif 'top_cards' in incoming_event and 'bottom_cards' in incoming_event:
    # positioning cards
    top_cards = _get_cards(lb, incoming_event['top_cards'])
    bottom_cards = _get_cards(lb, incoming_event['bottom_cards'])
    lb.cards = top_cards + lb.cards + bottom_cards
    lb.put()
    response = {'scry': True}
  
  return (response, notification)