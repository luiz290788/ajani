var search = angular.module('search', ['ui.bootstrap']);

search.controller('searchCtrl', ['$scope', '$http',
  function($scope, $http) {

    $scope.resultCards = [];

    $scope.emptyField= function() {
      $scope.selectedCard = '';
    }

    $scope.cardSearch = function(inputed) {
      $scope.setLoading(true);

      var promise = $http.get('/card', {'params':{'q': inputed}});
      promise.success(function(data) {
        $scope.resultCards = data.cards;
        $scope.setLoading(false);
      }).error(function() {
        $scope.resultCards = [];
        $scope.setLoading(false);
      });
      
      return promise;
    }
  }
]);
