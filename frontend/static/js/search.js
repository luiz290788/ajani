var search = angular.module('search', ['ui.bootstrap']);

search.controller('searchCtrl', ['$scope', '$http', '$q',
  function($scope, $http, $q) {

    $scope.resultCards = [];

    $scope.emptyField= function() {
      $scope.selectedCard = '';
    }

    $scope.cardSearch = function(inputed) {
      $scope.setLoading(true);

      var deferred = $q.defer();
      
      var promise = $http.get('/card', {'params':{'q': inputed}});
      promise.success(function(data) {
        $scope.resultCards = data.cards;
        $scope.setLoading(false);
        deferred.resolve(data.cards);
      }).error(function() {
        $scope.resultCards = [];
        $scope.setLoading(false);
        deferred.reject([]);
      });
      
      return deferred.promise;
    }
  }
]);
