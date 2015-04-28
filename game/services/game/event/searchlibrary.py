from google.appengine.ext import ndb
from services.model import Library

def search_library_process(game, player_id, incoming_event):
  lb = ndb.Key(Library, player_id, parent=game.key).get()
  response = {'library': {'cards': [card.to_dict() for card in lb.cards]}}

  return (response, None)