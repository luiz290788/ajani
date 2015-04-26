import random
from google.appengine.ext import ndb
from services import deckservices
from services.model import Library, Card

def generate(game, player_id):
  if game.player_0 == player_id:
    deck_id = game.deck_player_0
  elif game.player_1 == player_id:
    deck_id = game.deck_player_1
  
  deck = deckservices.get(deck_id)
  
  library_key = ndb.Key(Library, player_id, parent=game.key)
  library = Library(key=library_key, cards=[])
  
  card_instance = 0
  for multiverse_id, count in deck['cards'].iteritems():
    for times in range(count):  # @UnusedVariable
      card = Card(multiverse_id=multiverse_id, instance_id=card_instance)
      library.cards.append(card)
      card_instance = card_instance + 1

  random.shuffle(library.cards)

  library.put()
  return library

def get(game, player_id):
  library = ndb.Key(Library, player_id, parent=game.key).get()
  if library is None:
    library = generate(game, player_id)
  return library

def draw(library, hand_obj, count=1):
  hand_obj.cards.extend(library.cards[0:count])
  library.cards = library.cards[count:]
  ndb.put_multi([hand_obj, library])
  
  return hand_obj
