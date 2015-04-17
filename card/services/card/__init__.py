CARD_INDEX_NAME = 'MagicCards'

from google.appengine.ext import ndb
from services.model import MagicCard

def get_card(multiverseid):
  return ndb.Key(MagicCard, multiverseid).get()