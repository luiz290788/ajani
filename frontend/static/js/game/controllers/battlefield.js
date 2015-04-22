(function(angular) {
  
  angular.module('wd.game')
    .controller('battleFieldCtrl', battleFieldCtrl);
  
  battleFieldCtrl.$inject = ['$scope', '$routeParams', 'gameservices', '$cookies'];
  
  function battleFieldCtrl($scope, $routeParams, gameservices, $cookies) {
    var vm = this;

    vm.gameId = $routeParams.id;
    
    connect(vm.gameId);
    
    function connect(gameId) {
      var callback = function(token) {
        $cookies[gameId] = token;
        vm.token = token;
        openSocket(vm.token);
      }
      if ($cookies[gameId]) {
        callback($cookies[gameId]);
      } else {
        gameservices.connect(gameId).then(function(response) {
          var token = response.data.token;
          console.log(token);
          callback(token);
        });
      }
    }
    
    function openSocket(token) {
      vm.channel = new goog.appengine.Channel(token);
      vm.socket = vm.channel.open();
      
      vm.socket.onMessage = function(message) {
        console.log(message);
      };
    };
  };
  
})(angular);