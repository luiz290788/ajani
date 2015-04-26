(function(angular) {
  
  angular.module('wd.game')
    .controller('openHandCtrl', openHandCtrl);
  
  openHandCtrl.$inject = ['$scope', '$mdDialog', 'gameservices'];
  
  function openHandCtrl($scope, $mdDialog, gameservices) {
    var vm = this;
    
    getOpenHand();
    
    function getOpenHand() {
      gameservices.openHand($scope.gameId, $scope.player).then(function (response) {
        vm.cards = response.data.cards; 
      });
    }
  }
})(angular);