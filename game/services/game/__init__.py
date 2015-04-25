from services.model import Game, Event, Hand
from google.appengine.ext import ndb
from google.appengine.api import channel
from datetime import datetime
from services.game import state, event
import json

def _generate_token(game_id, player_num):
  return '%d-player-%d' % (game_id, player_num)

def create(kind):
  (game_id, _) = Game.allocate_ids(size=1)
  game = Game(key=ndb.Key(Game, game_id), kind=kind,
        token_player_0=_generate_token(game_id, 0),
        token_player_1=_generate_token(game_id, 1),
        created_at=datetime.now(),
        state = state.SELECT_DECK)

  game.put()
  
  return game

@ndb.transactional(retries=1)
def connect(urlsafe_id):
  game = ndb.Key(urlsafe=urlsafe_id).get()
  token = ''
  player = ''
  if game.player_0 is None:
    # player 0 is opening a connection
    game.player_0 = 'player_0'
    game.put()
    token = game.token_player_0
    player = 'player_0'
  elif game.player_1 is None:
    #player 1 is opening a connection
    game.player_1 = 'player_1'
    game.put()
    token = game.token_player_1
    player = 'player_1'
  else:
    #everybody is connected.
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
def process_event(game, player_id, incoming_event):
  event.save(game, player_id, incoming_event)

  processor = event.get_processor(incoming_event['event'])
  (response, notification) = processor(game, player_id, incoming_event)
  send_notifications(game, player_id, notification)

  return response




