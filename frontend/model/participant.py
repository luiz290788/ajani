from google.appengine.ext import ndb

class Participant(ndb.Model):
  gPlusId = ndb.StringProperty(required=True)
  # deck = ndb.StructuredProperty(MagicDeck)
