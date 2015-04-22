(function(angular) {
  
  angular.module('wd.game')
    .factory('gameservices', gameservices);
  
  gameservices.$inject = ['$http'];
  
  function gameservices($http) {
    return {
      create: create,
      connect: connect
    };
    
    function create(kind) {
      return $http.put('/api/game/' + kind);
    }
    
    function connect(id) {
      return $http.post('/api/game/' + id);
    }
  };
  
})(angular);