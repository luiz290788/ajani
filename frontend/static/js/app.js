var app = angular.module('app', [
  'ngRoute',
  'header',
  'dashboard',
  'deckManager',
  'search',
  'tournament'
]);

app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);

    $routeProvider.when('/dashboard', {
      templateUrl: '/partials/dashboard.html',
      controller: 'dashboardCtrl'
    }).when('/deck/add', {
      templateUrl: '/partials/adddeck.html',
      controller: 'addDeckCtrl'
    }).when('/tournament/:tournament_id', {
      templateUrl: '/partials/tournament.html',
      controller: 'tournamentCtrl'
    }).when('/deck', {
      templateUrl: '/partials/deckmanager.html',
      controller: 'deckManagerCtrl'
    }).otherwise({
      redirectTo: '/dashboard'
    })
}])
