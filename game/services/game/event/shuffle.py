from google.appengine.ext import ndb
from services.model import Library
import random
from services.game import response_util

def shuffle_process(game, player_id, incoming_event):
  lb = ndb.Key(Library, player_id, parent = game.key).get()
  random.shuffle(lb.cards)
  lb.put()
  
  library_response = response_util.library_response(lb)
  
  response = {'library': library_response}
  notification = {'opponent_library': library_response}
  
  return response, notification
  