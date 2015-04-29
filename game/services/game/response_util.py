
def library_response(library):
  response = {'cards': len(library.cards)}
  
  if library.top_revealed:
    response['top'] = library.cards[0].to_dict()
  
  return response

def card_response(card, opponent=False):
  response = card.to_dict()
  if opponent and (card.morph or card.manifest):
    response.pop('multiverse_id')
  return response

def battlefield_response(battlefield, opponent=False):
  cards = [card_response(card, opponent) for card in battlefield.cards]
  response = {'cards': cards}  
  return response