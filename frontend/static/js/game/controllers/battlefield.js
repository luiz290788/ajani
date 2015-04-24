(function(angular) {
  
  angular.module('wd.game')
    .controller('battleFieldCtrl', battleFieldCtrl);
  
  battleFieldCtrl.$inject = ['$scope', '$routeParams', 'gameservices', '$cookies', '$mdDialog'];
  
  function battleFieldCtrl($scope, $routeParams, gameservices, $cookies, $mdDialog) {
    var vm = this;

    vm.gameId = $routeParams.id;
    
    connect(vm.gameId);
    
    $scope.$watch('vm.state', function(newState, oldState) {
      switch (newState) {
      case 'select_deck':
        selectDeck();
        break;
      }
    });
    
    $scope.$on('socket.message', function(event, notification) {
      if (notification.state) {
        vm.state = notification.state;
      }
      $scope.$apply();
    });
    
    function connect(gameId) {
      var callback = function(identification) {
        $cookies[gameId] = angular.toJson(identification);
        vm.token = identification.token;
        vm.player = identification.player;
        openSocket(vm.token);
      }
      if ($cookies[gameId]) {
        callback(angular.fromJson($cookies[gameId]));
      } else {
        gameservices.connect(gameId).then(function(response) {
          callback(response.data);
        });
      }
    }
    
    function openSocket(token) {
      vm.channel = new goog.appengine.Channel(token);
      vm.socket = vm.channel.open();
      
      vm.socket.onmessage = function(message) {
        // TODO deal with messages
        notification = angular.fromJson(message.data);
        $scope.$emit('socket.message', notification);
      };
      
      vm.socket.onopen = function() {
        getState();
      };
    }
    
    function getState() {
      gameservices.getState(vm.gameId, vm.player).then(setState);
    }
    
    function selectDeck() {
      $mdDialog.show({
        controller: 'deckSelectorCtrl',
        controllerAs: 'vm',
        templateUrl: '/partials/deck/selector.html'
      }).then(function(deck) {
        gameservices.selectDeck(vm.gameId, vm.player, deck).then(setState);
      });
    }
    
    function setState(response) {
      vm.state = response.data.state;
    }
  };
  
})(angular);