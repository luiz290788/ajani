(function(angular) {
  angular.module('wd.game')
    .controller('opponentHandCtrl', opponentHandCtrl);
  
  opponentHandCtrl.$inject = ['$scope', 'hand', '$mdDialog'];
  
  function opponentHandCtrl($scope, hand, $mdDialog) {
    var vm = this;
    vm.opponentHand = hand;
    
    vm.close = function() {
      $mdDialog.hide();
    };
  }
})(angular);