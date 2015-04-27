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

    controller.$inject = ['$scope'];
    
    return directive;
    
    function controller($scope) {
      var vm = this;
      vm.card = $scope.card;
    }
    
    function link(scope, element, attr) {
      
    }
  };
  
})(angular);