(function(angular) {
  angular.module('wd.game')
    .controller('scryCtrl', scryCtrl);
  
  scryCtrl.$inject = ['$scope', '$mdDialog', 'gameservices', 'gameId', 'player']
  
  function scryCtrl($scope, $mdDialog, gameservices, gameId, player) {
    var vm = this;
    vm.gameId = gameId;
    vm.player = player;
    
    vm.getCards = function(count) {
      gameservices.scry(vm.gameId, vm.player, {'count': count}).then(function(response) {
        vm.cards = response.data.scry.cards;
        vm.cards.push({'library': true});
      });
    };
    
    vm.save = function(cards) {
      var topCards = [];
      var bottomCards = [];
      var libraryFound = false;
      for (card_index in cards) {
        var card = cards[card_index];
        if (card.library) {
          libraryFound = true;
        } else if (libraryFound) {
          bottomCards.push(card);
        } else {
          topCards.push(card);
        }
      }
      
      var toInstanceId = function(card) {return card.instance_id};
      
      gameservices.scry(vm.gameId, vm.player, {
        'top_cards': topCards.map(toInstanceId),
        'bottom_cards': bottomCards.map(toInstanceId)
      }).then(function(response) {
        if (response.data.scry) {
          $mdDialog.hide();
        }
      })
    };
  }
})(angular);