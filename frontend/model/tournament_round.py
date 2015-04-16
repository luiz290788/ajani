from datetime import datetime

from google.appengine.ext import ndb

class TournamentMatch(ndb.Model):
  # TODO, change user type to string to save entity key
  user_1 = ndb.StringProperty(required=True)
  score_1 = ndb.IntegerProperty()
  user_2 = ndb.StringProperty(required=True)
  score_2 = ndb.IntegerProperty()

class TournamentRound(ndb.Model):
  # parent = Tournament.key()
  number = ndb.IntegerProperty(required=True)
  matches = ndb.StructuredProperty(TournamentMatch, repeated=True)
  start_date = ndb.DateTimeProperty()

  @ndb.transactional()
  def start(self):
    tournament = self.key.parent().get()
    tournament.state = 3
    tournament.put()

    self.start_date = datetime.utcnow()
    self.put()

  def _post_put_hook(self, future):
    tournament = self.key.parent().get()

    round_done = True
    for match in self.matches:
      if match.score_1 != 2 and match.score_2 != 2:
        round_done = False

    if round_done :
      tournament.end_round()
