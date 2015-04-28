from google.appengine.ext import ndb
from services.model import BattleField, Graveyard, Exile, Hand, Library
import random

def _get_entity(entity_id):
  if entity_id == 'battlefield':
    entity = BattleField
  elif entity_id == 'graveyard':
    entity = Graveyard
  elif entity_id == 'exile':
    entity = Exile
  elif entity_id == 'hand':
    entity = Hand
  elif entity_id == 'library':
    entity = Library
  return entity

def _get_card_holders(game, player_id, ca_from, ca_to):
  from_entity = _get_entity(ca_from)
  to_entity = _get_entity(ca_to)
  from_key = ndb.Key(from_entity, player_id, parent=game.key)
  to_key = ndb.Key(to_entity, player_id, parent=game.key)
  objs = ndb.get_multi([from_key, to_key]);
  return (objs[0], objs[1])

def _entity_response(entity, hide_cards):
  if type(entity) in hide_cards:
    response = {'cards': len(entity.cards)}
  else:
    response = {'cards': [card.to_dict() for card in entity.cards]}

  return response

def move_process(game, player_id, incoming_event):
  from_entity = incoming_event['from']
  to_entity = incoming_event['to']
  (ca_from, ca_to) = _get_card_holders(game, player_id, from_entity, to_entity)
  
  if type(incoming_event['card']) in [int, long]:
    cards = [incoming_event['card']]
  elif type(incoming_event['card']) is list:
    cards = incoming_event['card']
  for card_id in cards:
    print card_id
    card = ca_from.get_card(card_id)
    ca_from.cards.remove(card)
    ca_to.cards.append(card)

  if type(ca_from) is Library:
    random.shuffle(ca_from.cards)
  
  ndb.put_multi([ca_from, ca_to])

  hide_cards = [Library]
  from_response = _entity_response(ca_from, hide_cards)
  to_response = _entity_response(ca_to, hide_cards)
  
  hide_opponent_cards = [Hand, Library]
  from_notification = _entity_response(ca_from, hide_opponent_cards)
  to_notification = _entity_response(ca_to, hide_opponent_cards)

  response = {from_entity: from_response, to_entity: to_response}
  notification = {'opponent_' + from_entity: from_notification,
                  'opponent_' + to_entity: to_notification}
  
  return (response, notification)