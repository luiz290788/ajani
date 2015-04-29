(function(angular) {
  
  angular.module('wd.card')
    .controller('revealCardCtrl', revealCardCtrl);
  
  revealCardCtrl.$inject = ['$scope', '$mdDialog', 'card']
  
  function revealCardCtrl($scope, $mdDialog, card) {
    var vm = this;
    vm.card = card;
    
    vm.close = function() {
      $mdDialog.hide();
    };
  }
  
})(angular);