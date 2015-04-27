from abc import abstractmethod

from google.appengine.ext import ndb

from services.game.event import selectdeck, throwdice, muligan, keep, playcard, \
  draw
from services.model import Event


SELECT_DECK = 'select_deck'
THROW_DICE = 'throw_dice'
MULIGAN = 'muligan'
KEEP = 'keep'
PLAY = 'play'
DRAW = 'draw'

processors = {}
  
def save(game, player_id, incoming_event):
  event = Event(parent = game.key, data = incoming_event, player_id = player_id)
  event.put()

def get_processor(event_type):
  return processors[event_type]

def _init_processors():
  processors[SELECT_DECK] = selectdeck.select_deck_process
  processors[THROW_DICE] = throwdice.throw_dice_process
  processors[MULIGAN] = muligan.muligan_process
  processors[KEEP] = keep.keep_process
  processors[PLAY] = playcard.play_card_proces
  processors[DRAW] = draw.draw_process
    
_init_processors()