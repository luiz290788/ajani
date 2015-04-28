from abc import abstractmethod

from google.appengine.ext import ndb

from services.game.event import selectdeck, throwdice, muligan, keep, draw, life, move, \
  tap, searchlibrary, shuffle, scry
from services.model import Event


SELECT_DECK = 'select_deck'
THROW_DICE = 'throw_dice'
MULIGAN = 'muligan'
KEEP = 'keep'
DRAW = 'draw'
LIFE = 'life'
MOVE = 'move'
TAP = 'tap'
UNTAP = 'untap'
UNTAP_ALL = 'untap_all'
SEARCH_LIBRARY = 'search_library'
SHUFFLE = 'shuffle'
SCRY = 'scry'

processors = {}
  
def save(game, player_id, incoming_event):
  event = Event(parent=game.key, data=incoming_event, player_id=player_id)
  event.put()

def get_processor(event_type):
  return processors[event_type]

def _init_processors():
  processors[SELECT_DECK] = selectdeck.select_deck_process
  processors[THROW_DICE] = throwdice.throw_dice_process
  processors[MULIGAN] = muligan.muligan_process
  processors[KEEP] = keep.keep_process
  processors[DRAW] = draw.draw_process
  processors[LIFE] = life.lifecounter_process
  processors[MOVE] = move.move_process
  processors[TAP] = tap.tap_process
  processors[UNTAP] = tap.untap_process
  processors[UNTAP_ALL] = tap.untap_all_process
  processors[SEARCH_LIBRARY] = searchlibrary.search_library_process
  processors[SHUFFLE] = shuffle.shuffle_process
  processors[SCRY]  = scry.scry_process
    
_init_processors()
