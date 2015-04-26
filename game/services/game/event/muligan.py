from services.game import hand, library

def muligan_process(game, player_id, incoming_event):
  hand_obj = hand.get(game.key, player_id)
  current_size = len(hand_obj.cards)
  
  library_obj = library.get(game, player_id)
  library_obj.cards.extend(hand_obj.cards)  
  library.shuffle(library_obj)
  hand_obj.cards = []

  library.draw(library_obj, hand_obj, current_size - 1)
  
  response = {'cards': [card.to_dict() for card in hand_obj.cards]}
  notification = None
  
  return (response, notification)