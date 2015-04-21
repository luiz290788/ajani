(function() {
  
var app = angular.module('web-duels', ['ngRoute',
                                       'wd.card',
                                       'wd.deck',
                                       'wd.game',
                                       'ngMaterial', 
                                       'ngAnimate', 
                                       'ngAria']);
  
  app.config(['$routeProvider', '$locationProvider',
              function($routeProvider, $locationProvider) {
    
    $locationProvider.html5Mode(true);
    
    $routeProvider.when('/deck/add', {
      templateUrl: '/partials/deck/add.html',
      controller: 'addDeckCtrl',
      controllerAs: 'vm'
    }).when('/deck/:id', {
      templateUrl: '/partials/deck/view.html',
      controller: 'viewDeckCtrl',
      controllerAs: 'vm'
    }).when('/deck/:id/edit', {
      templateUrl: '/partials/deck/edit.html',
      controller: 'editDeckCtrl',
      controllerAs: 'vm'
    }).when('/deck', {
      templateUrl: '/partials/deck/list.html',
      controller: 'listDeckCtrl',
      controllerAs: 'vm'
    }).when('/game/new', {
      templateUrl: '/partials/game/new.html',
      controller: 'newGameCtrl',
      controllerAs: 'vm'
    }).otherwise({
      redirectTo: '/deck'
    })
  }]);

})();

