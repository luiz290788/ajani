(function(angular) {
  
  angular.module('wd.util')
    .controller('dialogCtrl', dialogCtrl);
  
  dialogCtrl.$inject = ['$scope', '$mdDialog'];
  
  function dialogCtrl($scope, $mdDialog) {
    var vm = this;
    
    vm.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }
  
})(angular);