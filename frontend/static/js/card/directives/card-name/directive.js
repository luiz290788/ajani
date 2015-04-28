(function(angular) {
  angular.module('wd.card')
    .directive('wdCardName', wdCardName);
  
  function wdCardName() {
    var directive = {
      link: link,
      scope: {
        'multiverseId': '='
      },
      restrict: 'E',
      templateUrl: '/js/card/directives/card-name/template.html',
      controller: controller,
      controllerAs: 'vm'
    };
    
    controller.$inject = ['$scope', 'cardservices'];
    
    return directive;
    
    function controller($scope, cardservices) {
      var vm = this;
      vm.multiverseId = $scope.multiverseId;
      vm.name = "loading...";
      
      loadCard(vm.multiverseId);
      
      function loadCard(multiverseId) {
        cardservices.get(multiverseId).then(function(response) {
          vm.card = response.data;
          vm.name = vm.card.name;
        });
      }
    }
    
    function link(scope, element, attributes) {
      
    }
  }
})(angular);