from google.appengine.ext import ndb
from services.model import BattleField, Hand

def _get_objs(game, player_id):
  battlefield_key = ndb.Key(BattleField, player_id, parent=game.key)
  hand_key = ndb.Key(Hand, player_id, parent=game.key)
  objs = ndb.get_multi([battlefield_key, hand_key])
  
  return (objs[0], objs[1])

def play_card_proces(game, player_id, incoming_event):
  incoming_event['card']
  (bf, hand) = _get_objs(game, player_id)

  card = hand.get_card(incoming_event['card'])
  hand.cards.remove(card)
  bf.cards.append(card)
  
  ndb.put_multi([hand, bf])
  
  battlefield_resopnse = {'cards': [card.to_dict() for card in bf.cards]}
  hand_response = {'cards': [card.to_dict() for card in hand.cards]}
  opponent_hand = {'cards': len(hand.cards)}
  
  response = {'battlefield': battlefield_resopnse, 'hand': hand_response}
  notification = {'opponent_battlefield': battlefield_resopnse, 
                  'opponent_hand': opponent_hand}
  
  return (response, notification)