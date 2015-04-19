(function(angular) {
  angular.module('wd.deck')
    .controller('viewDeckCtrl', viewDeckCtrl);
  
  viewDeckCtrl.$inject = ['$scope', 'deckservices', '$routeParams', 'cardservices', '$location'];

  function viewDeckCtrl($scope, deckservices, $routeParams, cardservices, $location) {
    var vm = this;

    loadDeck($routeParams.id);
    
    $scope.$watch('vm.deck', function(newValue, oldValue) {
      if (newValue !== undefined) {
        sortCards(newValue);
      }
    });
    
    vm.edit = function(deck) {
      $location.path('/deck/' + deck.id + '/edit');
    };
    
    function loadDeck(id) {
      deckservices.load(id).then(function(response) {
        vm.deck = response.data;
      });
    }
    
    function addCard(category, card) {
      category.cards.push(card);
      category.total += card.copies;
    }
    
    function sortCards(deck) {
      vm.cards = {
        total: 0,
        lands: {cards:[], total: 0},
        creatures: {cards:[], total: 0},
        planeswalkers: {cards:[], total: 0},
        other: {cards:[], total: 0}
      };
      for (card_id in deck.cards) {
        vm.cards.total += deck.cards[card_id];
        
        cardservices.get(card_id).then(function(response) {
          var card = response.data;
          card.copies = deck.cards[card.multiverseid];
          switch (true) {
          case isType(card, 'Land'):
            addCard(vm.cards.lands, card)
            break;
          case isType(card, 'Creature'):
            addCard(vm.cards.creatures, card)
            break;
          case isType(card, 'Planeswalker'):
            addCard(vm.cards.planeswalkers, card)
            break;
          default:
            addCard(vm.cards.other, card)
          }
        });
      }
    }
    
    function isType(card, type) {
      for (var i in card.types) {
        if (card.types[i] == type) {
          return true;
        }
      }
      return false;
    }
  }
})(angular);