from google.appengine.ext import ndb

from services.model import Library


def load(incoming_event, player_id, game_key):
  return [ndb.Key(Library, player_id, parent=game_key)]

def process(incoming_event, player_id, game, lb):
  response = {'library': {'cards': [card.to_dict() for card in lb.cards]}}

  return (response, None, None)