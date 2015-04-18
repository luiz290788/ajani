(function(angular) {
  angular.module('wd.deck')
    .directive('wdCardListItem', wdCardListItem);
  
  function wdCardListItem() {
    var directive = {
      link: link,
      scope: {
        'id': '=',
        'copies': '='
      },
      restrict: 'E',
      templateUrl: '/js/deck/directives/card-list-item/template.html',
      controller: controller,
      controllerAs: 'vm'
    };
    
    controller.$inject = ['$scope', 'cardservices'];
    
    return directive;
    
    function controller($scope, cardservices) {
      var vm = this;
      
      vm.loadCard = function(id) {
        cardservices.get(id).then(function(response) {
          $scope.card = response.data;
        });
      };
      
      vm.removeCopy = function() {
        $scope.copies--;
      };
      
      vm.addCopy = function() {
        console.log($scope.card);
        if ($scope.card.rarity == 'Basic Land') {
          $scope.copies++;
        } else {
          $scope.copies = Math.min(4, $scope.copies + 1);
        }
      };

      $scope.$watch('id', function(newValue, oldValue) {
        vm.loadCard(newValue);
      });
      
      $scope.$watch('copies', function(newValue, oldValue) {
        $scope.$emit('wd.copiesChanged', 
            {'id': $scope.id, 'copies': $scope.copies});
      });
    }
    
    function link(scope, element, attr) {
      
    }
  }
  
})(angular);