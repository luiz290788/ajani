(function(angular) {
  
  angular.module('wd.game')
    .controller('cardActionsCtrl', cardActionsCtrl);
  
  cardActionsCtrl.$inject = ['$scope', '$mdDialog', 'actions'];
  
  function cardActionsCtrl($scope, $mdDialog, actions) {
    var vm = this;
    vm.actions = actions;
    
    vm.action = function(action) {
      $mdDialog.hide(action);
    };
  }
})(angular);