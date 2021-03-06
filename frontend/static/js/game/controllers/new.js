(function(angular) {
  
  angular.module('wd.game')
    .controller('newGameCtrl', newGameCtrl);
  
  newGameCtrl.$inject = ['$scope', '$location', '$mdDialog', 'gameservices'];
  
  function newGameCtrl($scope, $location, $mdDialog, gameservices) {
    var vm = this;
    
    showGameTypeSelector();
    function showGameTypeSelector() {
      
      $mdDialog.show({
        controller: 'dialogCtrl',
        controllerAs: 'vm',
        templateUrl: '/partials/game/selector.html'
      }).then(function(answer) {
        if (answer == 'standard') {
          gameservices.create(answer).then(function(response) {
            var game_id = response.data.game_id;
            $location.path('/game/' + game_id);
          });
        } else {
          showGameTypeSelector();
        }
      }, function() {
        showGameTypeSelector();
      });
    }
  }
})(angular);