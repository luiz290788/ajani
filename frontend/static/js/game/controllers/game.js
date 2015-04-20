(function(angular) {
  
  angular.module('wd.game')
    .controller('gameCtrl', gameCtrl);
  
  gameCtrl.$inject = ['$scope'];
  
  function gameCtrl($scope) {
    var vm = this;

    function openConnection() {
      vm.channel = new goog.appengine.Channel(vm.token);
      vm.socket = vm.channel.open();
      
      vm.socket.onMessage = function(message) {
        // TODO
      };
    };
  };
  
})(angular);