(function(angular) {
  angular.module('wd.game')
    .controller('diceCtrl', diceCtrl);
  
  diceCtrl.$inject = ['$scope', 'gameservices'];

  function diceCtrl($scope, gameservices) {
    var vm = this;
    
    $scope.$on('socket.message', function(event, notification) {
      vm.opponent_value = notification.dice_value;
      $scope.$apply();
    });
    
    vm.throwDice = function() {
      gameservices.throwDice($scope.gameId, $scope.player).then(function(response) {
        vm.my_value = response.data.dice_value;
        if (response.data.state) {          
          $scope.$emit('wd.change_state', response.data.state);
        }
      });
    }
  }
})(angular);