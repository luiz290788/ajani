from google.appengine.ext import ndb

class MagicCard(ndb.Model):
  multiverse_id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  color = ndb.StringProperty(repeated=True)
  set = ndb.StringProperty(required=True)
  rarity = ndb.StringProperty(required=True)