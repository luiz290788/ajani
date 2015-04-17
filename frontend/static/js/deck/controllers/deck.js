(function(angular) {
  angular.module('wd.deck')
    .controller('addDeckCtrl', addDeckCtrl);
  
  addDeckCtrl.$inject = ['$scope'];

  function addDeckCtrl($scope) {
    var vm = this;
    vm.deck = {
        "name": "abzan"
    };
  }
})(angular);