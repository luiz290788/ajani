(function(angular) {
  
  angular.module('wd.game')
    .controller('battleFieldCtrl', battleFieldCtrl);
  
  battleFieldCtrl.$inject = ['$scope', '$routeParams', 'gameservices'];
  
  function battleFieldCtrl($scope, $routeParams, gameservices) {
    var vm = this;

    vm.gameId = $routeParams.id;
    
    connect(vm.gameId);
    
    function connect(gameId) {
      gameservices.connect(gameId).then(function(response) {
        vm.token = response.data.token;
        openConnection(vm.token);
      });
    }
    
    function openConnection(token) {
      vm.channel = new goog.appengine.Channel(token);
      vm.socket = vm.channel.open();
      
      vm.socket.onMessage = function(message) {
        console.log(message);
      };
    };
  };
  
})(angular);