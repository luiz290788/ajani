(function(angular) {
  angular.module('wd.deck')
    .controller('viewDeckCtrl', addDeckCtrl);
  
  addDeckCtrl.$inject = ['$scope', 'deckservices', '$routeParams'];

  function addDeckCtrl($scope, deckservices, $routeParams) {
    var vm = this;

    loadDeck($routeParams.id);

    function loadDeck(id) {
      deckservices.load(id).then(function(response) {
        console.log(response);
        vm.deck = response.data;
      });
    }
  }
})(angular);