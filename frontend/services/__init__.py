import endpoints

from config import CONFIG

from api import duels
from deck import DeckManager
from tournament import TournamentServices

services = endpoints.api_server(
  [duels], restricted=False)
