(function(angular) {
  angular.module('wd.card')
    .factory('cardservices', cardservices);
  
  cardservices.$inject = ['$http'];
  
  function cardservices($http) {
    return {
      search: search
    };
    
    function search(term) {
      return $http.get('/card', {params: {q: term}});
    }
  }
})(angular);