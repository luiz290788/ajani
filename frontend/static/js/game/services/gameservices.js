(function(angular) {
  
  angular.module('vm.game')
    .factory('gameservices', gameservices);
  
  gameservices.$inject = ['$http'];
  
  function gameservices($http) {
    return {
      create: create
    };
    
    function create() {
      return $http.post('/api/game');
    }
  };
  
})(angular);