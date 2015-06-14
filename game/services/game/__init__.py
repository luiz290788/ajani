from services.model import Game, Event, Hand
from google.appengine.ext import ndb
from google.appengine.api import channel
from datetime import datetime
from services.game import state, event
import json, uuid

def _generate_token(game_id, player_num):
  return '%s-player-%d' % (game_id, player_num)

def create(kind):
  game_id = str(uuid.uuid4())
  game = Game(key=ndb.Key(Game, game_id), kind=kind,
        token_player_0=_generate_token(game_id, 0),
        token_player_1=_generate_token(game_id, 1),
        created_at=datetime.now(),
        state=state.SELECT_DECK)

  game.put()
  
  return game

@ndb.transactional(retries=1)
def connect(game_key):
  game = game_key.get()
  token = ''
  player = ''
  if game.player_0 is None:
    # player 0 is opening a connection
    game.player_0 = 'player_0'
    game.put()
    token = game.token_player_0
    player = 'player_0'
  elif game.player_1 is None:
    # player 1 is opening a connection
    game.player_1 = 'player_1'
    game.put()
    token = game.token_player_1
    player = 'player_1'
  else:
    # everybody is connected.
    # TODO think how to handle it
    pass
  return (token, player)

def send_notifications(game, player_id, notification):
  if notification is not None:
    if game.player_0 == player_id:
      token = game.token_player_1
    else:
      token = game.token_player_0
    channel.send_message(token, json.dumps(notification))

@ndb.transactional()
def process_event(game_key, player_id, incoming_event):
  (load, processor) = event.get_processor(incoming_event['event'])

  to_load = [game_key]
  if load is not None:
    to_load = to_load + load(incoming_event, player_id, game_key)
  loaded_entities = ndb.get_multi(to_load)
  game = loaded_entities[0]
  process_params = [incoming_event, player_id] + ndb.get_multi(to_load)
  
  (response, notification, to_put) = processor(*process_params)
  event_obj = Event(parent=game.key, data=incoming_event, player_id=player_id)
  if to_put is not None:
    to_put.append(event_obj)
  else:
    to_put = [event_obj]
  ndb.put_multi(to_put)
  send_notifications(game, player_id, notification)
  return response


