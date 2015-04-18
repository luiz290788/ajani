(function(angular) {
  angular.module('wd.deck')
    .factory('deckservices', deckservices);
  
  deckservices.$inject = ['$http'];
  
  function deckservices($http) {
    return {
      create: create,
      load: load,
      update: update
    };
    
    function load(id) {
      return $http.get('/api/deck/' + id);
    }
    
    function create(deck) {
      return $http.put('/api/deck', deck);
    }
    
    function update(deck) {
      return $http.post('/api/deck/' + deck.id, deck);
    }
  }
})(angular);