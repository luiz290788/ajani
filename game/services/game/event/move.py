from google.appengine.ext import ndb
from services.model import BattleField, Graveyard, Exile, Hand

def _get_entity(entity_id):
  if entity_id == 'battlefield':
    entity = BattleField
  elif entity_id == 'graveyard':
    entity = Graveyard
  elif entity_id == 'exile':
    entity = Exile
  elif entity_id == 'hand':
    entity = Hand
  return entity

def _get_card_holders(game, player_id, ca_from, ca_to):
  from_entity = _get_entity(ca_from)
  to_entity = _get_entity(ca_to)
  from_key = ndb.Key(from_entity, player_id, parent=game.key)
  to_key = ndb.Key(to_entity, player_id, parent=game.key)
  objs = ndb.get_multi([from_key, to_key]);
  return (objs[0], objs[1])

def move_process(game, player_id, incoming_event):
  from_entity = incoming_event['from']
  to_entity = incoming_event['to']
  (ca_from, ca_to) = _get_card_holders(game, player_id, from_entity, to_entity)
  
  card = ca_from.get_card(incoming_event['card'])
  ca_from.cards.remove(card)
  ca_to.cards.append(card)
  
  ndb.put_multi([ca_from, ca_to]);

  from_response = {'cards': [card.to_dict() for card in ca_from.cards]}
  to_response = {'cards': [card.to_dict() for card in ca_to.cards]}
  
  if from_entity == 'hand':
    from_notification = {'cards': len(ca_from.cards)}
  else:
    from_notification = from_response
  
  if to_entity == 'hand':
    to_notification = {'cards': len(ca_to.cards)}
  else:
    to_notification = to_response

  response = {from_entity: from_response, to_entity: to_response}
  notification = {'opponent_' + from_entity: from_notification,
                  'opponent_' + to_entity: to_notification}
  
  return (response, notification)