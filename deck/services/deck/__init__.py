import logging
from google.appengine.ext import ndb
from services.model import Deck

log = logging.getLogger(__name__)

def create(deck):
  deck.put()
  return deck

def get(deck_id):
  key = ndb.Key(Deck, deck_id)
  return key.get()

def update(deck_id, deck_obj):
  key = ndb.Key(Deck, deck_id)
  deck_obj.key = key
  deck_obj.put()
  return deck_obj


def delete(deck_id):
  key = ndb.Key(Deck, deck_id)
  key.delete()

