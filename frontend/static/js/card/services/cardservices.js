(function(angular) {
  angular.module('wd.card')
    .factory('cardservices', cardservices);
  
  cardservices.$inject = ['$http'];
  
  function cardservices($http) {
    return {
      search: search,
      get: get
    };
    
    function search(term) {
      return $http.get('/api/card', {params: {q: term}});
    }
    
    function get(id) {
      return $http.get('/api/card/' + id);
    }
  }
})(angular);