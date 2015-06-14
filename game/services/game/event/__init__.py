from abc import abstractmethod

from google.appengine.ext import ndb

from services.game.event import selectdeck, throwdice, muligan, keep, draw, life, move, \
  tap, searchlibrary, shuffle, scry, reveal
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
REVEAL_HAND = 'reveal_hand'
REVEAL_TOP = 'reveal_top'
REVEAL_CARD = 'reveal_card'

processors = {}

def get_processor(event_type):
  return processors[event_type]

def _init_processors():
  processors[SELECT_DECK] = (None, selectdeck.process)
  processors[THROW_DICE] = (None, throwdice.process)
  processors[MULIGAN] = (muligan.load, muligan.process)
  processors[KEEP] = (keep.load, keep.process)
  processors[DRAW] = (draw.load, draw.process)
  processors[LIFE] = (None, life.process)
  processors[MOVE] = (move.load, move.process)
  processors[TAP] = (tap.load, tap.process)
  processors[UNTAP] = (tap.load, tap.untap_process)
  processors[UNTAP_ALL] = (tap.load, tap.untap_all_process)
  processors[SEARCH_LIBRARY] = (searchlibrary.load, searchlibrary.process)
  processors[SHUFFLE] = (shuffle.load, shuffle.process)
  processors[SCRY] = (scry.load, scry.process)
  processors[REVEAL_HAND] = (reveal.hand_load, reveal.hand_process)
  processors[REVEAL_TOP] = (reveal.top_load, reveal.top_process)
  processors[REVEAL_CARD] = (reveal.card_load, reveal.card_process)
    
_init_processors()
