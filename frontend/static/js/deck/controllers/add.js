(function(angular) {
  angular.module('wd.deck')
    .controller('addDeckCtrl', addDeckCtrl);
  
  addDeckCtrl.$inject = ['$scope', 'deckservices', '$location', '$mdToast'];

  function addDeckCtrl($scope, deckservices, $location, $mdToast) {
    var vm = this;
    vm.deck = {};
    
    vm.saveDeck = function(deck) {
      deckservices.create(deck).then(function(response) {
        $location.path('/deck/' + response.data.id);
        $mdToast.show(
          $mdToast.simple()
            .content('Deck created succesfully!')
            .hideDelay(3000)
        );
        console.log(response);
      });
    };
  }
})(angular);