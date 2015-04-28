(function(angular) {
  
  angular.module('wd.game')
    .controller('searchLibraryCtrl', searchLibraryCtrl);
  
  searchLibraryCtrl.$inject = ['$scope', '$mdDialog', 'gameservices', 'gameId', 'player'];
  
  function searchLibraryCtrl($scope, $mdDialog, gameservices, gameId, player) {
    var vm = this;
    vm.gameId = gameId;
    vm.player = player;
    vm.selectedCards = [];

    getLibrary();
    
    vm.close = function() {
      gameservices.shuffle(gameId, player).then(function(response) {
        $mdDialog.hide();
      });
    };
    
    vm.move = function(to) {
      if (vm.selectedCards.length) {
        $scope.$emit('wd.move', vm.selectedCards, ['library', to]);
        $mdDialog.hide();
      } else {
        vm.close();
      }
    };
    
    vm.selectCard = function(card) {
      vm.library.cards = vm.library.cards.filter(function(x) {
        return x.instance_id != card.instance_id;
      });
      vm.selectedCards.push(card);
    };
    
    function getLibrary() {
      gameservices.searchLibrary(vm.gameId, vm.player).then(function(response) {
        vm.library = response.data.library;
      });
    }
  }
})(angular);