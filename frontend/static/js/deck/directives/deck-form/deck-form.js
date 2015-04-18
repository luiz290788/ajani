(function(angular) {
  
  angular.module('wd.deck')
    .directive('wdDeckForm', wdDeckForm);
  
  function wdDeckForm() {
    var directive = {
      restrict: 'E',
      link: link,
      templateUrl: '/js/deck/directives/deck-form/deck-form.html',
      scope: {},
      require: '^ngModel',
      controller: controller,
      controllerAs: 'vm'
    };
    
    controller.$inject = ['$scope', '$q', 'cardservices']
    
    return directive;
    
    function controller($scope, $q, cardservices) {
      var vm = this;
      
      vm.resetCard = function() {
        vm.searchText = "";
        vm.selectedCard = false;
        vm.copies = 1;
      }

      vm.searchCards = function(term) {
        var deferred = $q.defer();
        cardservices.search(term).then(function(response) {
          deferred.resolve(response.data.cards);
        });

        return deferred.promise;
      };
      
      vm.setCard = function(card) {
        vm.selectedCard = card;
      };
      
      vm.addCard = function() {
        var id = vm.selectedCard.multiverse_id;
        
        if (!$scope.deck.cards) {
          $scope.deck.cards = {};
        }

        var copies = vm.copies;
        if ($scope.deck.cards[id]) {
          copies = $scope.deck.cards[id] + copies;
        }
        $scope.deck.cards[id] = Math.min(4, copies);
        
        vm.resetCard();
      };
      
      $scope.$on('wd.copiesChanged', function(event, args) {
        if (args.copies <= 0) {          
          delete $scope.deck.cards[args.id];
        } else {
          $scope.deck.cards[args.id] = args.copies;
        }
      });
      
      vm.resetCard();
    }
    
    function link(scope, element, attr, ngModel) {
      ngModel.$render = function() {
        scope.deck = ngModel.$viewValue;
      };
    }
  }
  
})(angular);