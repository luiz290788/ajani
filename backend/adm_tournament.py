import webapp2
import jinja2
import math

from datetime import datetime

from model import Tournament, Participant, User
from config import CONFIG
from user import getPersonalInfo

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(CONFIG['templates_dir']))

class AdmTournament(webapp2.RequestHandler):

  @staticmethod
  def participants_display_name(participants):
    participants_info = []
    for participant in participants:
      user_info = getPersonalInfo(participant)
      if user_info:
        participants_info.append({
          'id': participant.gPlusId,
          'name': user_info['displayName']
        })
      else:
        participants_info.append({
          'id': participant.gPlusId,
          'name': participant.gPlusId
        })
    return participants_info

  def render_tournament_page(self):
    tournament = self.get_tournament()

    if tournament:
      num_enrolled = len(tournament.participants)
      available_seats = tournament.max_num_participants - num_enrolled

      tournament.num_enrolled = num_enrolled
      tournament.available_seats = available_seats

      if self.request.get("round"):

        round = tournament.get_round(int(self.request.get("round")))

        if round:
          matches = []
          for obj_match in round.matches:
            match = {}

            # User 1
            user_1_info = getPersonalInfo(obj_match.user_1)
            try:
              match['user_1_name'] = \
                user_1_info['name']['firstName'] + ' ' + user_1_info['name']['lastName']
            except:
              match['user_1_name'] = obj_match.user_1

            # User 2
            if not obj_match.user_2:
              match['user_2_name'] = 'Bye'
            else:
              user_2_info = getPersonalInfo(obj_match.user_2)
              try:
                match['user_2_name'] = \
                  user_2_info['name']['firstName'] + ' ' + user_2_info['name']['lastName']
              except:
                match['user_2_name'] = obj_match.user_2

            # Set the score, in case of Bye consider a 2-0
            if not obj_match.user_2:
              match['user_1_score'] = 2
              match['user_2_score'] = 0
            else:
              match['user_1_score'] = obj_match.score_1
              match['user_2_score'] = obj_match.score_2
            matches.append(match)

          self.template_values['completed_rounds'] = tournament.get_tournament_rounds()
          self.template_values['matches'] = matches
          self.template_values['round_start_date'] = round.start_date

      self.template_values['tournament'] = tournament
      
      self.template_values['participants_to_render'] = \
        AdmTournament.participants_display_name(tournament.participants)

      tournament.get_leaderboard()

      template = jinja_environment.get_template('adm_tournament.template')
      self.response.out.write(template.render(self.template_values))

    else:
      self.redirect('/backend/tournament')

  def get(self):
    self.template_values = {}

    # If no tournament was selected, show the list and form to create new ones
    if not self.request.get("tournament-key"):
      tournaments = Tournament.query().order(Tournament.date_time).fetch(20)
      for tournament in tournaments:
        tournament.participants_to_render = \
          AdmTournament.participants_display_name(tournament.participants)
      self.template_values['tournaments'] = tournaments

      template = jinja_environment.get_template('adm_tournaments.template')
      self.response.out.write(template.render(self.template_values))

    # If a tournament was selected, show the tournament page
    else:
      self.render_tournament_page()

  def get_tournament(self):
    tournament_id = self.request.get("tournament-key")

    return Tournament.get_by_urlsafe(tournament_id)

  def update_round(self):
    tournament = self.get_tournament()
    current_round = tournament.get_round(tournament.current_round)

    for i in xrange(1, len(current_round.matches) + 1):
      t_match = current_round.matches[i - 1]
      t_match.score_1 = int(self.request.get('user_' + str(i) + '_1'))
      t_match.score_2 = int(self.request.get('user_' + str(i) + '_2'))

    current_round.put()

  def create_tournament(self):
    d = self.request.get("tournament-date").split('-')
    t = self.request.get("tournament-time").split(':')

    tournament = Tournament(
      name = self.request.get('tournament-name'),
      date_time = datetime(int(d[0]), int(d[1]), int(d[2]), int(t[0]), int(t[1])),
      max_num_participants = int(self.request.get("tournament-participants")),
      round_duration = int(self.request.get('tournament-round-dur')),
      format = self.request.get('tournament-format'),
      participants = []
      # participants = [Participant(gPlusId='101221084281835829670'), \
      #   Participant(gPlusId='101221084281835829671'), Participant(gPlusId='101221084281835829669'), \
      #   Participant(gPlusId='101221084281835829673'), Participant(gPlusId='101221084281835829674'), \
      #   Participant(gPlusId='101221084281835829675'), Participant(gPlusId='101221084281835829676'), \
      #   Participant(gPlusId='101221084281835829677'), Participant(gPlusId='101221084281835829678'), \
      #   Participant(gPlusId='101221084281835829679'), Participant(gPlusId='101221084281835829680'), \
      #   Participant(gPlusId='101221084281835829681'), Participant(gPlusId='101221084281835829682'), \
      #   Participant(gPlusId='101221084281835829683')]
    )

    tournament.put()
    return tournament

  def post(self):
    redirect_to_page = ''
    tournament = self.get_tournament()

    op = self.request.get("op").lower()

    if op == 'create':
      tournament = self.create_tournament()
    elif op == 'generate matches':
      tournament.generate_round()
    elif op == 'start':
      current_round = tournament.get_round(tournament.current_round)
      current_round.start()
    elif op == 'save':
      self.update_round()
    elif op == 'end round':
      self.update_round()
      tournament.end_round()
    elif op == 'end tournament':
      tournament.end_tournament()
    elif op == 'remove user':
      user = User.get_by_id(self.request.get('user-id'))
      tournament.unsubscribe(user)
    elif op == 'delete tournament':
      tournament.delete_tournament()
      redirect_to_page = '/backend/static/tournament-deleted'

    if redirect_to_page:
      self.redirect(redirect_to_page)
    else:
      self.redirect('/backend/tournament?tournament-key=' + tournament.key.urlsafe() \
        + '&round=' + str(tournament.current_round))
