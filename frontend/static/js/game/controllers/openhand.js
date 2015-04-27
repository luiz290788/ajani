(function(angular) {
  
  angular.module('wd.game')
    .controller('openHandCtrl', openHandCtrl);
  
  openHandCtrl.$inject = ['$scope', '$mdDialog', 'gameservices'];
  
  function openHandCtrl($scope, $mdDialog, gameservices) {
    var vm = this;
    
    getOpenHand();
    
    vm.muligan = function() {
      gameservices.muligan($scope.gameId, $scope.player).then(setCardsCallback)
    };
    
    vm.keep = function() {
      gameservices.keep($scope.gameId, $scope.player).then(function (response) {
        $mdDialog.hide(response.data);
      });
    };
    
    function getOpenHand() {
      gameservices.openHand($scope.gameId, $scope.player).then(setCardsCallback);
    }
    
    function setCardsCallback(response) {
      vm.cards = response.data.cards;
    }
  }
})(angular);