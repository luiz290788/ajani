import endpoints
from endpoints import AUTH_LEVEL
from protorpc import remote, message_types

from google.appengine.ext import ndb

import messages
from model import MagicDeck, DeckCard, User
from auth_util import get_google_plus_user_id
from user import getUser
from api import duels

@duels.api_class(resource_name = 'deck', path = 'deck')
class DeckManager(remote.Service):

  @endpoints.method(messages.DeckMessage, messages.DeckMessage,
    path = '{deck_id}', http_method = 'GET', name = 'get',
    auth_level = AUTH_LEVEL.REQUIRED)
  def getDeck(self, deckMessage):
    # TODO use ResourceContainer

    # load deck data and return it
    # check if the deck is from current user
    key = ndb.Key(urlsafe = deckMessage.deck_id)
    deck = key.get()

    user = getUser()
    if deck.key.parent().id() == user.gPlusId:

      deckMessage.deck_name = deck.name

      deckMessage.cards = []
      for card in deck.cards:
        deckMessage.cards.append(messages.CardMessage(
          multiverse_id = card.multiverse_id,
          card_name = card.card_name,
          quantity = card.quantity
        ))

      deckMessage.land = messages.LandMessage(
        swamp = deck.swamp,
        island = deck.island,
        plains = deck.plains,
        forrest = deck.forrest,
        mountain = deck.mountain
      )

    return deckMessage

  @endpoints.method(message_types.VoidMessage, messages.DeckListMessage,
    path = 'my', http_method = 'GET', name = 'my',
    auth_level = AUTH_LEVEL.REQUIRED)
  def my(self, request):
    # load all decks of the current user
    user = getUser()

    results = MagicDeck.query(ancestor=user.key).fetch()

    deckMessages = []

    for deck in results:
      deckMessages.append(messages.DeckMessage(
        deck_id = deck.key.urlsafe(),
        deck_name = deck.name
      ))

    return messages.DeckListMessage(decks = deckMessages)

  @endpoints.method(messages.DeckMessage, messages.DeckMessage,
    path = 'save', http_method = 'POST', name = 'save',
    auth_level = AUTH_LEVEL.REQUIRED)
  def saveDeck(self, deck_message):
    user = getUser()
    if user is not None:

      if deck_message.deck_id is None:
        deck = MagicDeck(
          parent = user.key,
          name = deck_message.deck_name,
          swamp = deck_message.land.swamp,
          island = deck_message.land.island,
          plains = deck_message.land.plains,
          forrest = deck_message.land.forrest,
          mountain = deck_message.land.mountain,
          total_cards = 0 #TODO calculate total cards to store it
        )

        cards = []
        for card_message in deck_message.cards:
          cards.append(DeckCard(
            multiverse_id = card_message.multiverse_id,
            quantity = card_message.quantity
          ))

        deck.cards = cards
        deck.put()
      else:
        # TODO existing deck, update it
        pass
    else :
      # TODO raise an unauthorized exception
      pass
    return deck_message
