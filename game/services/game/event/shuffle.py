from google.appengine.ext import ndb
from services.model import Library
import random
from services.game import response_util

def load(incoming_event, player_id, game_key):
  return [ndb.Key(Library, player_id, parent = game_key)]

def process(incoming_event, player_id, game, lb):
  random.shuffle(lb.cards)
  
  library_response = response_util.library_response(lb)
  
  response = {'library': library_response}
  notification = {'opponent_library': library_response}
  
  return response, notification, [lb]
  