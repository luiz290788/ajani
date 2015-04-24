(function(angular) {
  angular.module('wd.game')
    .controller('diceCtrl', diceCtrl);
  
  diceCtrl.$inject = ['$scope', 'gameservices'];

  function diceCtrl($scope, gameservices) {
    var vm = this;
    
    vm.throwDice = function() {
      gameservices.throwDice($scope.gameId, $scope.player).then(function(response) {
        console.log(response);
      });
    }
  }
})(angular);