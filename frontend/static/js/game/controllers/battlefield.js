(function(angular) {
  
  angular.module('wd.game')
    .controller('battleFieldCtrl', battleFieldCtrl);
  
  battleFieldCtrl.$inject = ['$scope', '$routeParams', 'gameservices', '$cookies', '$mdDialog'];
  
  function battleFieldCtrl($scope, $routeParams, gameservices, $cookies, $mdDialog) {
    var vm = this;
    vm.opponent = {};
    vm.gameId = $routeParams.id;
    
    connect(vm.gameId);
    
    $scope.$watch('vm.state', function(newState, oldState) {
      switch (newState) {
      case 'select_deck':
        selectDeck();
        break;
      case 'throw_dice':
        throwDice();
        break;
      case 'opening_hand':
        if (!vm.diceDialog) {
          openHand();
        }
        break;
      }
    });
    
    $scope.$on('socket.message', function(event, notification) {
      if (notification.state) {
        vm.state = notification.state;
      }
      if (notification.opponent_hand) {
        vm.opponent.hand = notification.opponent_hand;
      }
      if (notification.opponent_library) {
        vm.opponent.library = notification.opponent_library;
      }
      if (notification.opponent_battlefield) {
        vm.opponent.battlefield = notification.opponent_battlefield;
      }
      if (notification.opponent_life) {
        vm.opponent.life = notification.opponent_life;
      }
      $scope.$apply();
    });

    $scope.$on('wd.change_state', function(event, state) {
      vm.state = state;
    });

    $scope.$on('wd.move', function(event, card, args) {
      var from = args[0];
      var to = args[1];
      gameservices.move(vm.gameId, vm.player, card.instance_id, from, to).then(function (response) {
        var data = response.data;
        if (data.hand) {
          vm.hand = data.hand;
        }
        if (data.battlefield) {
          vm.battlefield = data.battlefield;
        }
        if (data.graveyard) {
          vm.graveyard = data.graveyard;
        }
        if (data.exile) {
          vm.exile = data.exile;
        }
      });
    });

    vm.draw = function() {
      gameservices.draw(vm.gameId, vm.player).then(function(response) {
        vm.library = response.data.library;
        vm.hand = response.data.hand;
      });
    };
    
    vm.changeLife = function(delta) {
      gameservices.life(vm.gameId, vm.player, delta).then(function(response) {
        vm.life = response.data.life
      });
    };
    
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
        notification = angular.fromJson(message.data);
        $scope.$broadcast('socket.message', notification);
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
    
    function throwDice() {
      var newScope = $scope.$new(true, $scope);
      newScope.gameId = vm.gameId;
      newScope.player = vm.player;
      vm.diceDialog = $mdDialog.show({
        scope: newScope,
        controller: 'diceCtrl',
        controllerAs: 'vm',
        templateUrl: '/partials/game/dice.html'
      });
      
      vm.diceDialog.then(openHand);
    }
    
    function setState(response) {
      var data = response.data

      vm.state = data.state;
      vm.opponent.library = data.opponent_library;
      vm.opponent.hand = data.opponent_hand;
      vm.library = data.library;
      vm.hand = data.hand;
      vm.battlefield = data.battlefield;
      vm.opponent.battlefield = data.opponent_battlefield;
      vm.life = data.life;
      vm.opponent.life = data.opponent_life;
    }
    
    function openHand() {
      var newScope = $scope.$new(true, $scope);
      newScope.gameId = vm.gameId;
      newScope.player = vm.player;
      vm.openHandDialog = $mdDialog.show({
        scope: newScope,
        controller: 'openHandCtrl',
        controllerAs: 'vm',
        templateUrl: '/partials/game/openhand.html'
      });
      
      vm.openHandDialog.then(function(openHand) {
        vm.hand = openHand.hand;
        vm.state = openHand.state;
        vm.library = openHand.library;
      });
    }
  };
  
})(angular);