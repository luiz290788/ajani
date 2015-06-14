import random

from google.appengine.ext import ndb

from services.game import response_util
from services.model import BattleField, Graveyard, Exile, Hand, Library


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

def _get_card_holders_keys(game_key, player_id, ca_from, ca_to):
  from_entity = _get_entity(ca_from)
  to_entity = _get_entity(ca_to)
  from_key = ndb.Key(from_entity, player_id, parent=game_key)
  to_key = ndb.Key(to_entity, player_id, parent=game_key)
  return [from_key, to_key]

def _entity_response(entity, hide_cards, opponent=False):
  if type(entity) is Library:
    response = response_util.library_response(entity)
  if type(entity) is BattleField:
    response = response_util.battlefield_response(entity, opponent)
  elif type(entity) in hide_cards:
    response = {'cards': len(entity.cards)}
  else:
    response = {'cards': [card.to_dict() for card in entity.cards]}

  return response

def _set_flags(ca_to, card, options):
  if type(ca_to) is BattleField:
    card.tapped = options.get('tapped', False)
    card.morph = options.get('morph', False)
    card.manifest = options.get('manifest', False)
  else:
    card.tapped = False
    card.morph = False
    card.manifest = False
  
def load(incoming_event, player_id, game_key):
  from_entity = incoming_event['from']
  to_entity = incoming_event['to']
  return _get_card_holders_keys(game_key, player_id, from_entity, to_entity)

def process(incoming_event, player_id, game, ca_from, ca_to):
  options = incoming_event['options']

  if options.get('manifest', False) and type(ca_from) is Library:
    cards = [ca_from.cards[0].instance_id]
  elif type(incoming_event['card']) in [int, long]:
    cards = [incoming_event['card']]
  elif type(incoming_event['card']) is list:
    cards = incoming_event['card']
  for card_id in cards:
    card = ca_from.get_card(card_id)
    ca_from.cards.remove(card)
    ca_to.cards.append(card)
    _set_flags(ca_to, card, options)

  if type(ca_from) is Library:
    random.shuffle(ca_from.cards)

  to_put = [ca_from, ca_to]

  hide_cards = [Library]
  from_response = _entity_response(ca_from, hide_cards)
  to_response = _entity_response(ca_to, hide_cards)

  hide_opponent_cards = [Hand, Library]
  from_notification = _entity_response(ca_from, hide_opponent_cards, opponent=True)
  to_notification = _entity_response(ca_to, hide_opponent_cards, opponent=True)


  from_entity = incoming_event['from']
  to_entity = incoming_event['to']
  response = {from_entity: from_response, to_entity: to_response}
  notification = {'opponent_' + from_entity: from_notification,
                  'opponent_' + to_entity: to_notification}

  return (response, notification, to_put)
