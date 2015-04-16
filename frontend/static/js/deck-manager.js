var deckManager = angular.module('deckManager', []);


deckManager.controller('deckManagerCtrl', ['$scope', '$location', '$q',
  function($scope, $location, $q) {

    $scope.decks = {};

    $scope.loadDecks = function() {
      $scope.setLoading(true);

      var deferred = $q.defer();

      gapi.client.request({
        'path': '/duels/v1/deck/my',
        'root': apisRoot
      }).execute(function(response) {
        deferred.resolve(response)
      });

      deferred.promise.then(function(response) {
        $scope.decks = response.decks;
        $scope.setLoading(false);
      })
    };

    $scope.$watch(
      'ready',
      function(newValue, oldValue) {
        if (newValue) {
          if (!$scope.loggedIn) {
            $location.path('/dashboard');
          } else {
            $scope.loadDecks();
          }
        }
      }
    )

  }
]).controller('addDeckCtrl', ['$scope',
  function($scope) {

    $scope.updateTotalCards = function() {
      $scope.totalCards = 0;
      for (land in $scope.deck.land) {
        $scope.totalCards += $scope.deck.land[land];
      }
      for (card in $scope.deck.cards) {
        $scope.totalCards += $scope.deck.cards[card].quantity;
      }
    };

    $scope.addCard = function(card) {
      if (!$scope.deck.cards[card.multiverse_id]) {
        card.quantity = 1;
        $scope.deck.cards[card.multiverse_id] = card;
        $scope.updateTotalCards();
      }
    }

    $scope.removeCard = function(card) {
      delete $scope.deck.cards[card.multiverse_id];
      $scope.updateTotalCards();
    }

    $scope.saveDeck = function(deck) {
      $scope.setLoading(true);
      var cards = [];

      for (id in deck.cards) {
        cards.push(deck.cards[id]);
      }

      deck.cards = cards;

      gapi.client.request({
        'root': apisRoot,
        'path': '/duels/v1/deck/save',
        'method': 'POST',
        'body': deck
      }).execute(function(resp) {
        $scope.setLoading(false);
      })
    }

    $scope.deck = {
      cards: {},
      land: {
        swamp: 0,
        island: 0,
        plains: 0,
        forrest: 0,
        mountain: 0
      },
      deck_name: '',
      deck_id: null
    }

    $scope.totalCards = 0;

    $scope.updateTotalCards();
  }
]);
