from __future__ import division
from decimal import Decimal
import math
import logging
from random import randrange

from google.appengine.ext import ndb
from google.appengine.api import memcache

from model import Participant, TournamentRound, TournamentMatch

class Tournament(ndb.Model):
  name = ndb.StringProperty(required=True)
  date_time = ndb.DateTimeProperty(required=True)
  max_num_participants = ndb.IntegerProperty(required=True)
  max_rounds = ndb.IntegerProperty(required=True)
  round_duration = ndb.IntegerProperty(required=True)
  available_seats = ndb.IntegerProperty(required=True)
  # Round State
  # state = 1 => [TODO] Matches not generated yet. Actions: generate matches
  # state = 2 => [READY] Round not started yet. Actions: start
  # state = 3 => [WIP] Round in progress. Actions: save, next round
  # state = 4 => [DONE] Round is finished. Actions: end tournament
  # state = 5 => [END] Tournament ended => Display champions
  state = ndb.IntegerProperty(required=True, default=1)
  current_round = ndb.IntegerProperty(required=True, default=0)
  format = ndb.StringProperty(required=True)
  participants = ndb.StructuredProperty(Participant, repeated=True)

  @staticmethod
  def get_by_urlsafe(urlsafe):
    tournament = None
    try:
      tournament = ndb.Key(urlsafe=urlsafe).get()
    except:
      logging.debug('Error loading tournament by urlsafe: %s'%urlsafe)

    return tournament

  def _pre_put_hook(self):
    if len(self.participants) > 0:
      self.max_rounds = int(math.ceil(math.log(len(self.participants), 2)))
    else:
      self.max_rounds = 0

    self.available_seats = self.max_num_participants - len(self.participants)

  @ndb.transactional(xg=True)
  def subscribe(self, user):
    user_subscribed = False

    if self.state is 1 and \
        len(self.participants) < self.max_num_participants:
      user_found = False
      for participant in self.participants:
        if participant.gPlusId == user.gPlusId:
          user_found = True
          break

      if not user_found:
        self.participants.append(Participant(gPlusId = user.gPlusId));
        self.put()

        if not user.tournaments_subscribed:
          user.tournaments_subscribed = []
        user.tournaments_subscribed.append(self.key.urlsafe())
        user.put()

        user_subscribed = True

    return user_subscribed

  @ndb.transactional(xg=True)
  def unsubscribe(self, user):

    user.tournaments_subscribed.remove(self.key.urlsafe())
    user.put()

    for participant in self.participants:
      if participant.gPlusId == user.gPlusId:
        self.participants.remove(participant)

    self.put()

  def get_tournament_rounds(self):
    rounds = []
    for i in xrange(1, self.current_round + 1):
      rounds.append(self.get_round(i))
    return rounds

  def get_round(self, round_number):
    query = TournamentRound.query(ancestor=self.key)\
      .filter(TournamentRound.number == round_number)

    return query.get()

  # Possible return:
  #   0:  Draw
  #   1:  User 1 won
  #   2:  User 2 won
  @staticmethod
  def get_match_result(match):
    if match.score_1 == 2 or (match.score_1 == 1 and match.score_2 == 0):
      return 1
    elif (match.score_1 == 0 and match.score_2 == 0) or \
      (match.score_1 == 1 and match.score_2 == 1):
      return 0
    else:
      return 2

  def check_duplicate_match(self, user_1, user_2):
    for i in xrange(1, self.current_round + 1):
      round = self.get_round(i)
      for match in round.matches:
        if (match.user_1 == user_1['user_id'] and match.user_2 == user_2['user_id']) or \
          (match.user_1 == user_2['user_id'] and match.user_2 == user_1['user_id']):
          return True

    return False

  @staticmethod
  def compare_score(a, b):
    # Reference, http://users.ipfw.edu/buldtb/private/fwgg/mtg/pdfs/MTR.pdf
    # First criteria, Players Match Points 
    if a['match_points'] != b['match_points']:
      return b['match_points'] - a['match_points']

    # Second criteria, Opponents Match-win Percentage
    elif a['opponents_match_win_percentage'] != b['opponents_match_win_percentage']:
      if a['opponents_match_win_percentage'] > b['opponents_match_win_percentage']:
        return -1
      elif b['opponents_match_win_percentage'] > a['opponents_match_win_percentage']:
        return 1

    # Third criteria, Player Game-win Percentage
    elif a['game_win_percentage'] != b['game_win_percentage']:
      if a['game_win_percentage'] > b['game_win_percentage']:
        return -1
      elif b['game_win_percentage'] > a['game_win_percentage']:
        return 1

    # Fourth criteria, Opponents Game-win Percentage
    elif a['opponents_game_win_percentage'] != b['opponents_game_win_percentage']:
      if a['opponents_game_win_percentage'] > b['opponents_game_win_percentage']:
        return -1
      elif b['opponents_game_win_percentage'] > a['opponents_game_win_percentage']:
        return 1
    return 0 

  def get_leaderboard(self):
    if self.current_round:
      leaderboard = {}

      for participant in self.participants:

        leaderboard[participant.gPlusId] = {
          'user_id': participant.gPlusId,
          'ranking': 0,
          'match_points': 0,
          'matches_played': 0,
          'match_win_percentage': 0.0,
          'games_won': 0,
          'games_lost': 0,
          'game_points': 0,
          'game_win_percentage': 0.0,
          'games_played': 0,
          'opponents': [],
          'opponents_match_win_percentage': 0.0,
          'opponents_game_win_percentage': 0.0
        }

      # 1. Sum up Match and Game Points
      self.leaderboard_sum_matches_and_games(leaderboard)

      leaderboard_values = leaderboard.values()

      # 2. Calculate the Percentages for each user
      self.leaderbard_calculate_player_percentages(leaderboard_values)
      
      # 3. Calculate Opponents Match-win and Game-win Percentages for each user
      self.leaderboard_calculate_opponents_percentages(leaderboard_values, leaderboard)

      # 4. Sort all players based on score
      leaderboard_values.sort(cmp=Tournament.compare_score)

      # 5. Fil up rankings
      self.leaderboard_ranking(leaderboard_values)

      # DEBUG, maybe transform into a log to debug in production
      for player in leaderboard_values:
        print str(player['ranking']) + ' - ' + str(player['user_id']) + ': ' + str(player['match_points']) + ' ' + \
          str(player['opponents_match_win_percentage']) + ' ' + \
          str(player['game_win_percentage']) + ' ' + \
          str(player['opponents_game_win_percentage']) + ' => ' + \
          str(player['match_win_percentage'])

      t_key = self.key.urlsafe()
      memcache.set('tournament-leaderboard-' + t_key, leaderboard_values)
      return leaderboard_values

  def leaderboard_sum_matches_and_games(tournament, leaderboard):
    for i in xrange(1, tournament.current_round + 1):
      round = tournament.get_round(i)

      for match in round.matches:
        result = Tournament.get_match_result(match)
        user_1_index = match.user_1
        user_2_index = match.user_2

        # 1.1. Player Match Points. Give it to whoever won
        # [FORMULA] PMP = 3 * match_wins + 0 * match_losses + 1 * match_draws
        if result == 1:
          leaderboard[user_1_index]['match_points'] += 3
        elif result == 2:
          # No need to test for Bye index, as he will never win
          leaderboard[user_2_index]['match_points'] += 3

        # In case of Draw, give 1 point each
        else:
          leaderboard[user_1_index]['match_points'] += 1
          if user_2_index in leaderboard:
            leaderboard[user_2_index]['match_points'] += 1

        # 1.2. Sum up Games Won and Lost
        leaderboard[user_1_index]['games_won'] += match.score_1
        leaderboard[user_1_index]['games_lost'] += match.score_2
        if user_2_index in leaderboard:
          leaderboard[user_2_index]['games_won'] += match.score_2
          leaderboard[user_2_index]['games_lost'] += match.score_1


        # 1.3. Player Game Points, each game won is 3 points
        # [FORMULA] Player Game Points = 3 * game_wins + 0 * game_losses
        leaderboard[user_1_index]['game_points'] += match.score_1 * 3
        if user_2_index in leaderboard:
          leaderboard[user_2_index]['game_points'] += match.score_2 * 3

        # 1.4. Build opponents list
        # Test user 2 to check if it is a Bye. Currently, if its the case the 
        # Bye will always appear in the last seat of the tournment, always user 2.
        # If Bye, dont include in opponents since its metrics doesn't count on 
        # opponents percentages
        if user_2_index in leaderboard:
          leaderboard[user_1_index]['opponents'].append(leaderboard[user_2_index]['user_id'])
          leaderboard[user_2_index]['opponents'].append(leaderboard[user_1_index]['user_id'])

        # 1.5. Sum up Matches and Games Played
        leaderboard[user_1_index]['matches_played'] += 1
        leaderboard[user_1_index]['games_played'] += match.score_1 + match.score_2
        if user_2_index in leaderboard:
          leaderboard[user_2_index]['matches_played'] += 1
          leaderboard[user_2_index]['games_played'] += match.score_1 + match.score_2

  def leaderbard_calculate_player_percentages(self, leaderboard_values):
    for player in leaderboard_values:
      if player['matches_played'] > 0 and player['games_played'] > 0:
        # [FORMULA] Player Match-win Percentage = Player Match Points / 3 * Matches Played
        player['match_win_percentage'] = \
          player['match_points'] / (3 * player['matches_played'])
        # [FORMULA] Player Game-win Percentage = Player Game Points / 3 * Games Played
        player['game_win_percentage'] = \
          player['game_points'] / (3 * player['games_played'])

  def leaderboard_calculate_opponents_percentages(self, leaderboard_values, leaderboard):
    for player in leaderboard_values:

      if len(player['opponents']) > 0:
        for opponent in player['opponents']:
          # As per Appendix D on the reference: "Establishing a minimum match-win 
          # percentage [0.33] limits the effect low performances have when calculating
          # and comparing opponents match-win percentages."
          if leaderboard[opponent]['match_win_percentage'] < 1 / 3:
            player['opponents_match_win_percentage'] += 1 / 3
          else:
            player['opponents_match_win_percentage'] += \
              leaderboard[opponent]['match_win_percentage']
          if leaderboard[opponent]['game_win_percentage'] < 1 / 3:
            player['opponents_game_win_percentage'] += 1 / 3
          else:
            player['opponents_game_win_percentage'] += \
              leaderboard[opponent]['game_win_percentage']

        # [FORMULA] OMWP = SUM(Opponent Match-win Percentage) / Number of Opponents
        player['opponents_match_win_percentage'] = \
          player['opponents_match_win_percentage'] / \
          len(player['opponents'])
        # [FORMULA] OGWP = SUM(Opponent Game-win Percentage) / Number of Opponents
        player['opponents_game_win_percentage'] = \
          player['opponents_game_win_percentage'] / \
          len(player['opponents'])

  def leaderboard_ranking(self, leaderboard_values):
    ranking = 1;
    num_players = len(leaderboard_values)
    for i in xrange(0, num_players):
      if i == 0:
        leaderboard_values[i]['ranking'] = ranking
        ranking = ranking + 1
      else:
        compare_result = self.compare_score(leaderboard_values[i - 1], leaderboard_values[i])
        if compare_result == 0:
          leaderboard_values[i]['ranking'] = leaderboard_values[i - 1]['ranking']
        else:
          leaderboard_values[i]['ranking'] = ranking
          ranking = ranking + 1

  def end_round(self):
    self.state = 4
    self.put()

  def end_tournament(self):
    self.state = 5
    self.put()

  def generate_first_round(tournament, num_matches):
    # tounrnament is about to start
    participants_aux = tournament.participants[:]
    match_list = []

    for i in xrange(0, num_matches):
      random_index = randrange(0, len(participants_aux))
      user_1 = participants_aux.pop(random_index)
      user_1_id = user_1.gPlusId

      # Check if we have an odd number of players
      # Empty user should be treated as Bye (aka free win)
      if len(participants_aux):
        random_index = randrange(0, len(participants_aux))
        user_2 = participants_aux.pop(random_index)
        user_2_id = user_2.gPlusId
      else:
        user_2 = 0
        user_2_id = ''

      match_list.append(TournamentMatch(
        user_1 = user_1_id,
        score_1 = 0,
        user_2 = user_2_id,
        score_2 = 0
      ))

    round = TournamentRound(
      parent = tournament.key,
      number = 1,
      matches = match_list
    )

    round.put()

    tournament.state = 2
    tournament.current_round = 1
    tournament.put()

  def generate_swiss_round(tournament, num_matches):
    # generate new round based on scores
    match_list = []

    # Get current leaderboard
    leaderboard = tournament.get_leaderboard()

    # Exclude duplicate matches
    for i in xrange(0, num_matches):
      user_1 = leaderboard.pop(0)
      y = 0
      while True:
        try:
          user_2 = leaderboard.pop(y)
          if tournament.check_duplicate_match(user_1, user_2):
            # If duplicated, put user back and try the next
            leaderboard.insert(y, user_2)
            y = y + 1
            continue
          else:
            # If not duplicated, just break of infinite loop
            break
        except:
          # Check if we have an odd number of players
          # ID 0 should be treated as Bye (aka free win)
          user_2 = {'user_id': ''}
          break

      match_list.append(TournamentMatch(
        user_1 = user_1['user_id'],
        score_1 = 0,
        user_2 = user_2['user_id'],
        score_2 = 0
      ))

    tournament.state = 2
    tournament.current_round = tournament.current_round + 1
    tournament.put()

    round = TournamentRound(
      parent = tournament.key,
      number = tournament.current_round,
      matches = match_list
    )

    round.put()

  @ndb.transactional()
  def generate_round(self):
    real_num_participants = len(self.participants)
    num_matches = int(math.ceil(real_num_participants/float(2)))

    if self.state == 1 :
      self.generate_first_round(num_matches)
    elif self.current_round < self.max_rounds :
      self.generate_swiss_round(num_matches)

    return round

  def delete_tournament(self):
    rounds = self.get_tournament_rounds()
    for round in rounds:
      round.key.delete()
    self.key.delete()