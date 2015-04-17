(function() {
  
var app = angular.module('web-duels', ['ngRoute',
                                       'wd.card',
                                       'wd.deck', 
                                       'ngMaterial', 
                                       'ngAnimate', 
                                       'ngAria']);
  
  app.config(['$routeProvider', '$locationProvider',
              function($routeProvider, $locationProvider) {
    
    $locationProvider.html5Mode(true);
    
    $routeProvider.when('/deck/add', {
      templateUrl: '/partials/adddeck.html',
      controller: 'addDeckCtrl',
      controllerAs: 'vm'
    }).otherwise({
      redirectTo: '/deck/add'
    })
  }]);

})();

