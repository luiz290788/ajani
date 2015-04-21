(function(angular) {
  
  angular.module('wd.game')
    .factory('gameservices', gameservices);
  
  gameservices.$inject = ['$http'];
  
  function gameservices($http) {
    return {
      create: create
    };
    
    function create(kind) {
      return $http.put('/api/game/' + kind);
    }
  };
  
})(angular);