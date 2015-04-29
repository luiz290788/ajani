(function(angular) {
  
  angular.module('wd.game')
    .directive('wdGameCard', wdGameCard);
  
  function wdGameCard() {
    var directive = {
      link: link,
      scope: {
        'card': '=',
        'placement': '@'
      },
      templateUrl: '/js/game/directives/game-card/template.html',
      controller: controller,
      controllerAs: 'vm'
    };

    controller.$inject = ['$scope', '$mdDialog'];
    
    return directive;
    
    function controller($scope, $mdDialog) {
      var vm = this;
      vm.card = $scope.card;
      vm.placement = $scope.placement;
      vm.readOnly = $scope.readOnly
      
      $scope.$watch('card', function(newCard) {
        vm.card = newCard;
      });
      
      $scope.$watch('vm.card.tapped', function(tapped) {
        if (tapped) {
          var rotate = 'rotate(90deg)';
          vm.style = {
            '-ms-transform': rotate,
            '-webkit-transform': rotate,
            'transform': rotate
          };
        } else {
          vm.style = {};
        }
      });
      
      vm.showActions = function($event) {
        var actions = getActions(vm.placement);
        if (actions && actions.length) {
          $mdDialog.show({
            targetEvent: $event,
            locals: {
              actions: actions
            },
            templateUrl: '/js/game/directives/game-card/card-actions.html',
            controller: 'cardActionsCtrl',
            controllerAs: 'vm'
          }).then(function(action) {
            var match = action.match(/([^\(\)]*?)\(([^\(\)]*)\)/);
            var prefix = 'wd.';
            if (match) {
              action = match[1];
              var params = match[2].split(',').map(function(x) { return x.trim()});
              $scope.$emit(prefix + action, vm.card, params);
            } else {
              $scope.$emit(prefix + action, vm.card);
            }
          });
        }
      };
      
      function action(key, label) {
        return {
          'key': key,
          'label': label
        };
      }
      
      function getActions(placement) {
        var actions = [];
        switch (placement) {
        case 'hand':
          actions.push(action('move(hand,battlefield)', 'Play'));
          actions.push(action('move(hand,battlefield,{"tapped":true})', 'Play tapped'));
          actions.push(action('move(hand,graveyard)', 'Discard'));
          actions.push(action('move(hand,exile)', 'Exile'));
          break;
        case 'battlefield':
          if (vm.card.tapped) {
            actions.push(action('untap', 'Untap'))
          } else {
            actions.push(action('tap', 'Tap'));
          }
          actions.push(action('move(battlefield,graveyard)', 'Put in graveyard'));
          actions.push(action('move(battlefield,exile)', 'Exile'));
          break;
        }
        return actions;
      }
    }
    
    function link(scope, element, attr) {
    }
  };
  
})(angular);