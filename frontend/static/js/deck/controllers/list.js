(function(angular) {
  angular.module('wd.deck')
    .controller('listDeckCtrl', listDeckCtrl);
  
  listDeckCtrl.$inject = ['$scope', 'deckservices', '$location', '$mdDialog', '$mdToast'];

  function listDeckCtrl($scope, deckservices, $location, $mdDialog, $mdToast) {
    var vm = this;

    listDecks();

    vm.add = function() {
      $location.path('/deck/add');
    };
    
    vm.view = function(deck) {
      $location.path('/deck/' + deck.id);
    };
    
    vm.edit = function(deck) {
      $location.path('/deck/' + deck.id + '/edit');
    };
    
    vm.delete = function(deck) {
      var confirm = $mdDialog.confirm()
        .parent(angular.element(document.body))
        .title('Are you sure you want to delete "' + deck.name + '" deck?')
        .content('This cannot be undone.')
        .ok('Yes')
        .cancel('No');
      $mdDialog.show(confirm).then(function() {
        deckservices.delete(deck.id).then(function(response) {
          listDecks();
          $mdToast.show(
            $mdToast.simple()
              .content('"' + deck.name + '" was successfully deleted!')
              .hideDelay(3000)
          );
        });
      });
    };
    
    function listDecks() {
      vm.decks = [];
      deckservices.list().then(function(response) {
        vm.decks = response.data.decks;
      });
    }
  }
})(angular);