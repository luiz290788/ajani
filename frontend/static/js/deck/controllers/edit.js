(function(angular) {
  angular.module('wd.deck')
    .controller('editDeckCtrl', addDeckCtrl);
  
  addDeckCtrl.$inject = ['$scope', 'deckservices', '$location', '$mdToast', '$routeParams'];

  function addDeckCtrl($scope, deckservices, $location, $mdToast, $routeParams) {
    var vm = this;
    
    loadDeck($routeParams.id);

    function loadDeck(id) {
      deckservices.load(id).then(function(response) {
        vm.deck = response.data;
      });
    }
    
    function gotoView() {
      $location.path('/deck/' + vm.deck.id);
    }
    
    vm.cancelEdit = function() {
      gotoView();
    };
    
    vm.updateDeck = function(deck) {
      deckservices.update(deck).then(function(response) {
        gotoView();
        $mdToast.show(
            $mdToast.simple()
            .content('Deck created succesfully!')
            .hideDelay(3000)
        );        
      });
    };
  }
})(angular);