(function(angular) {
  angular.module('wd.deck')
    .factory('deckservices', deckservices);
  
  deckservices.$inject = ['$http'];
  
  function deckservices($http) {
    return {
      create: create,
      load: load,
      update: update,
      list: list,
      'delete': delete_deck
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
    
    function list() {
      return $http.get('/api/deck');
    }
    
    function delete_deck(id) {
      return $http.delete('/api/deck/' + id)
    }
  }
})(angular);