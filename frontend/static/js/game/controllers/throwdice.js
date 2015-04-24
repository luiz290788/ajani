(function(angular) {
  angular.module('wd.game')
    .controller('diceCtrl', diceCtrl);
  
  diceCtrl.$inject = ['$scope', 'gameservices', '$mdDialog'];

  function diceCtrl($scope, gameservices, $mdDialog) {
    var vm = this;
    
    $scope.$watchGroup(['vm.my_value', 'vm.opponent_value'], function(dices) {
      if (dices[0] && dices[1]) {
        if (dices[0] != dices[1]) {          
          vm.go_first = dices[0] > dices[1];
          vm.opponent_go_first = !vm.go_first;
        } else {
          vm.throw_again = true;
        }
      }
    });
    
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
    };
    
    vm.close = function() {
      $mdDialog.hide();
    };
  }
})(angular);