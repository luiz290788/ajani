from abc import abstractmethod
from google.appengine.ext import ndb
from services.game.event import selectdeck
from services.model import Event

SELECT_DECK = 'select_deck'

processors = {}
  
def save(game, player_id, incoming_event):
  event = Event(parent = game.key, data = incoming_event, player_id = player_id)
  event.put()

def get_processor(event_type):
  return processors[event_type]

def _init_processors():
  processors[SELECT_DECK] = selectdeck.select_deck_process
    
_init_processors()