from google.appengine.ext import ndb

class MagicCard(ndb.Model):
  layout = ndb.StringProperty()
  name = ndb.StringProperty(required=True)
  names = ndb.StringProperty(repeated=True)
  mana_cost = ndb.StringProperty()
  cmc = ndb.IntegerProperty()
  colors = ndb.StringProperty(repeated=True)
  type = ndb.StringProperty()
  supertypes = ndb.StringProperty(repeated=True)
  types = ndb.StringProperty(repeated=True)
  subtypes = ndb.StringProperty(repeated=True)
  rarity = ndb.StringProperty()
  text = ndb.StringProperty()
  flavor = ndb.StringProperty()
  artist = ndb.StringProperty()
  number = ndb.StringProperty()
  power = ndb.StringProperty()
  toughness = ndb.StringProperty()
  loyalty = ndb.IntegerProperty()
  multiverseid = ndb.IntegerProperty()
  variations = ndb.IntegerProperty(repeated=True)
  image_name = ndb.StringProperty()
  watermark = ndb.StringProperty()
  border = ndb.StringProperty()
  timeshifted = ndb.BooleanProperty()
  hand = ndb.IntegerProperty()
  life = ndb.IntegerProperty()
  reserved = ndb.BooleanProperty()
  releasedate = ndb.StringProperty()
  starter = ndb.BooleanProperty()
  set = ndb.StringProperty(required=True)
  
  @classmethod
  def from_dict(cls, card_dict):
    card = MagicCard(
      id=card_dict['multiverseid']
    )
    
    if 'manaCost' in card_dict:
      card_dict['mana_cost'] = card_dict['manaCost']
      del card_dict['manaCost']
    if 'imageName' in card_dict:
      card_dict['image_name'] = card_dict['imageName']
      del card_dict['imageName']
    
    
    card.populate(**card_dict)
    return card