(function(angular) {
  
  angular.module('wd.deck')
    .controller('deckSelectorCtrl', deckSelectorCtrl);
  
  deckSelectorCtrl.$inject = ['$scope', 'deckservices', '$mdDialog'];
  
  function deckSelectorCtrl($scope, deckservices, $mdDialog) {
    var vm = this;
    
    loadDecks();
    
    function loadDecks() {
      deckservices.list().then(function(response) {
        vm.decks = response.data.decks;
      });
    }
    
    vm.answer = function(selectedDeck) {
      $mdDialog.hide(selectedDeck);
    };
  }
  
})(angular);