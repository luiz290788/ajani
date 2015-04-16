import endpoints
from endpoints import AUTH_LEVEL
from protorpc import remote, message_types
from google.appengine.api import memcache

import messages
from config import CONFIG
from model import Tournament, User, Participant
from user import getPersonalInfo, getUser
from api import duels

@duels.api_class(resource_name = 'tournament', path='tournament')
class TournamentServices(remote.Service):

  def _tournmanetToMessage(self, tournament, user = None):
    participantsMessages = []

    roundMessage = None

    if tournament.state == 1:
      for participant in tournament.participants:
        participant_user = User.get_by_id(participant.gPlusId)
        if not participant_user:
          participant_user = participant.gPlusId

        user_info = getPersonalInfo(participant_user)
        if user_info:
          participantsMessages.append(messages.ParticipantMessage(
            user_id = participant.gPlusId,
            name = user_info['name']['givenName'],
            image = user_info['image']['url']
          ))
    else:
      leaderboard = memcache.get(key='tournament-leaderboard-' + tournament.key.urlsafe())
      if not leaderboard:
        leaderboard = tournament.get_leaderboard()
      if leaderboard:
        for player in leaderboard:
          player_user = User.get_by_id(player['user_id'])
          if player_user:
            user_info = getPersonalInfo(player_user)
            participantsMessages.append(messages.ParticipantMessage(
              user_id = player['user_id'],
              name = user_info['name']['givenName'],
              image = user_info['image']['url'],
              ranking = player['ranking'],
              match_points = player['match_points'],
              opponents_match_win_percentage = '%.2f' % player['opponents_match_win_percentage'],
              game_win_percentage = '%.2f' % player['game_win_percentage'],
              opponents_game_win_percentage = '%.2f' % player['opponents_game_win_percentage'],
              games_played = player['games_played'],
              games_won = player['games_won'],
              games_lost = player['games_lost']
            ))
          else:
            participantsMessages.append(messages.ParticipantMessage(
              user_id = player['user_id'],
              name = player['user_id'],
              image = '/images/default-user.jpg',
              ranking = player['ranking'],
              match_points = player['match_points'],
              opponents_match_win_percentage = '%.2f' % player['opponents_match_win_percentage'],
              game_win_percentage = '%.2f' % player['game_win_percentage'],
              opponents_game_win_percentage = '%.2f' % player['opponents_game_win_percentage'],
              games_played = player['games_played'],
              games_won = player['games_won'],
              games_lost = player['games_lost']
            ))

      if tournament.state < 4:
        matchesMessages = []

        round = tournament.get_round(tournament.current_round)

        for match in round.matches:
          user1 = User.get_by_id(match.user_1)
          if not user1:
            user1 = match.user_1
          user1_info = getPersonalInfo(user1)
          if match.user_2 and match.user_2 != '0':
            user2 = User.get_by_id(match.user_2)
            if not user2:
              user2 = match.user_2
            user2_info = getPersonalInfo(user2)
          else:
            user2_info = {'name': {'givenName': 'Bye'}, 'image': {'url': '/images/default-user.jpg'}}

          matchesMessages.append(messages.MatchMessage(
            player1 = messages.ParticipantMessage(
              user_id = match.user_1,
              match_points = match.score_1,
              name = user1_info['name']['givenName'],
              image = user1_info['image']['url']
            ),
            player2 = messages.ParticipantMessage(
              user_id = match.user_2,
              match_points = match.score_2,
              name = user2_info['name']['givenName'],
              image = user2_info['image']['url']
            )
          ))
        roundMessage = messages.RoundMessage(
          number = round.number,
          matches = matchesMessages,
          start_date = round.start_date
        )

    user_subscribed = None
    if user and user.tournaments_subscribed and \
      tournament.key.urlsafe() in user.tournaments_subscribed:
      user_subscribed = True

    return messages.TournamentMessage(
      tournament_id = tournament.key.urlsafe(),
      name = tournament.name,
      status = tournament.state,
      date_time = tournament.date_time,
      participants = participantsMessages,
      current_round = roundMessage,
      round_duration = tournament.round_duration,
      user_subscribed = user_subscribed,
      available_seats = tournament.available_seats
    )

  @endpoints.method(message_types.VoidMessage, messages.TournamentListMessage,
    path = '/tournament', http_method = 'GET', name = 'all',
    auth_level = AUTH_LEVEL.OPTIONAL)
  def all(self, request):

    tournaments = Tournament.query().fetch()

    tournament_messages = []

    for tournament in tournaments:
      tournament_messages.append(messages.TournamentMessage(
        tournament_id = tournament.key.urlsafe(),
        name = tournament.name
      ))

    return messages.TournamentListMessage(tournaments = tournament_messages)

  @endpoints.method(messages.TOURNAMENT_RC, messages.TournamentMessage,
    path = '{tournament_id}', http_method = 'GET', name = 'get',
    auth_level = AUTH_LEVEL.OPTIONAL)
  def get(self, request):

    tournament = Tournament.get_by_urlsafe(request.tournament_id)

    #if not tournament:
      # Send message to redirect to dashboard page

    return self._tournmanetToMessage(tournament, getUser())

  @endpoints.method(messages.TOURNAMENT_RC, messages.TournamentMessage,
    path = '{tournament_id}/subscribe', http_method = 'GET',
    name = 'subscribe', auth_level = AUTH_LEVEL.REQUIRED)
  def subscribe(self, request):
    user = getUser()

    if user:
      tournament = Tournament.get_by_urlsafe(request.tournament_id)
      tournament.subscribe(user)

      return self._tournmanetToMessage(tournament, user)
