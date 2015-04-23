from services.model import Game
from google.appengine.ext import ndb
from datetime import datetime
from services.game import state, event

def _generate_token(game_id, player_num):
  return '%d-player-%d' % (game_id, player_num)

def create(kind):
  (game_id, _) = Game.allocate_ids(size=1)
  game = Game(key=ndb.Key(Game, game_id), kind=kind,
        token_player_0=_generate_token(game_id, 0),
        token_player_1=_generate_token(game_id, 1),
        created_at=datetime.now())

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
    # TODO thing how to handle it
    pass
  return (token, player)

def get_state(game_id, player_id):
  game = ndb.Key(urlsafe=game_id).get()
  response = {}
  if player_id == game.player_0 :
    if game.deck_player_0 is None:
      response['state'] = state.CHOOSE_DECK
    else:
      response['state'] = state.WAIT_OPPNENT
  elif player_id == game.player_1 :
    if game.deck_player_1 is None:
      response['state'] = state.CHOOSE_DECK
    else:
      response['state'] = state.WAIT_OPPNENT
      
  return response

@ndb.transactional()
def process_event(game_id, player_id, incoming_event):
  game = ndb.Key(urlsafe=game_id).get()
  response = {'state': state.CHOOSE_DECK}
  if incoming_event['event'] == event.SELECT_DECK:
    deck = incoming_event['deck']
    if player_id == game.player_0 :
      game.deck_player_0 = deck
    elif player_id == game.player_1 :
      game.deck_player_1 = deck
    game.put()
    response['state'] = state.WAIT_OPPNENT
    
  return response
