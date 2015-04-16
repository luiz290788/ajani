var apisRoot = '//' + window.location.host + '/_ah/api'

var header = angular.module('header', []);

function init() {
  window.init();
}

header.controller('headerCtrl', ['$scope', '$window', '$q',
  function($scope, $window, $q) {

    $scope.setLoading = function(value){
      if (value)
        $scope.loadingCount++;
      else if ($scope.loadingCount > 0)
        $scope.loadingCount--;
      $scope.loading = $scope.loadingCount > 0;
    };

    $scope.setUserInformation = function(token) {
      $scope.ready = true;
      if (token && token.status.signed_in && token.status.google_logged_in) {
        // user is logged in
        $scope.loggedIn = true;

        var deferred = $q.defer();

        gapi.client.request({
          'path': '/userinfo/v2/me'
        }).execute(function(resp) {
          deferred.resolve(resp)
        });

        deferred.promise.then(function(resp) {
          if (!resp.code) {

            var token = gapi.auth.getToken();
            token.access_token = token.id_token;
            gapi.auth.setToken(token);

            $scope.user = {
              imageUrl: resp.picture,
              name: resp.given_name
            };
            $scope.setLoading(false);
            $scope.loggedIn = true;
          }
        });

      } else {
        // user is not logged in
        $scope.setLoading(false);
      }
    }

    $scope.authorize = function() {
      $scope.setLoading(true);

      gapi.auth.signOut();

      var deferred = $q.defer();

      gapi.auth.authorize({
        client_id: "246410276514-19obm550uk64bf6io6itmj9n02on1aq7.apps.googleusercontent.com",
        scope: ['https://www.googleapis.com/auth/plus.login',
                'https://www.googleapis.com/auth/plus.me',
                'https://www.googleapis.com/auth/plus.profiles.read',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'],
              immediate: true, response_type: 'token id_token'},
              function(token) {
                deferred.resolve(token);
              });

      deferred.promise.then($scope.setUserInformation);
    }

    $window.init = function() {
      $scope.$apply($scope.authorize);
    }

    $scope.loggedIn = false;
    $scope.loading = true;
    $scope.loadingCount = 0;
    $scope.loggedIn = false;
    $scope.ready = false;
    $scope.user = {};

  }
]);
