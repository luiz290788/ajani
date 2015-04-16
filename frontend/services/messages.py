import endpoints

from protorpc import messages
from protorpc import message_types

TOURNAMENT_RC = endpoints.ResourceContainer(
  message_types.VoidMessage,
  tournament_id = messages.StringField(1, required=True)
)

CARD_SEARCH_RC = endpoints.ResourceContainer(
  message_types.VoidMessage,
  card_name = messages.StringField(1, required=True)
)

class CardMessage(messages.Message):
  multiverse_id = messages.StringField(1, required=True)
  card_name = messages.StringField(2)
  quantity = messages.IntegerField(3)

class SearchResultMessage(messages.Message):
  cards = messages.MessageField(CardMessage, 1, repeated=True)

class LandMessage(messages.Message):
  swamp = messages.IntegerField(1)
  island = messages.IntegerField(2)
  plains = messages.IntegerField(3)
  forrest = messages.IntegerField(4)
  mountain = messages.IntegerField(5)

class DeckMessage(messages.Message):
  deck_id = messages.StringField(1)
  deck_name = messages.StringField(2)
  land = messages.MessageField(LandMessage, 3)
  cards = messages.MessageField(CardMessage, 4, repeated=True)

class DeckListMessage(messages.Message):
  decks = messages.MessageField(DeckMessage, 1, repeated=True)

class ParticipantMessage(messages.Message):
  user_id = messages.StringField(1)
  name = messages.StringField(2)
  image = messages.StringField(3)
  ranking = messages.IntegerField(4)
  match_points = messages.IntegerField(5)
  opponents_match_win_percentage = messages.StringField(6)
  game_win_percentage = messages.StringField(7)
  opponents_game_win_percentage = messages.StringField(8)
  games_played = messages.IntegerField(9)
  games_won = messages.IntegerField(10)
  games_lost = messages.IntegerField(11)

class MatchMessage(messages.Message):
  player1 = messages.MessageField(ParticipantMessage, 1)
  player2 = messages.MessageField(ParticipantMessage, 2)

class RoundMessage(messages.Message):
  number = messages.IntegerField(1)
  start_date = message_types.DateTimeField(2)
  matches = messages.MessageField(MatchMessage, 3, repeated=True)

class TournamentMessage(messages.Message):
  tournament_id = messages.StringField(1)
  name = messages.StringField(2)
  status = messages.IntegerField(3)
  participants = messages.MessageField(ParticipantMessage, 4, repeated=True)
  date_time = message_types.DateTimeField(5)
  current_round = messages.MessageField(RoundMessage, 6)
  round_duration = messages.IntegerField(7)
  user_subscribed = messages.BooleanField(8)
  available_seats = messages.IntegerField(9)

class TournamentListMessage(messages.Message):
  tournaments = messages.MessageField(TournamentMessage, 1, repeated=True)
