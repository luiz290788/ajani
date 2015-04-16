var tournament = angular.module('tournament', []);

tournament.controller('tournamentCtrl', ['$scope', '$routeParams', '$interval', '$q',
  function($scope, $routeParams, $interval, $q) {
    $scope.isDetailsDisplayed = false;

    $scope.loadTournament = function(tournament_id) {
      var deferred = $q.defer();

      $scope.setLoading(true);
      gapi.client.request({
        'root': apisRoot,
        'path': '/duels/v1/tournament/' + tournament_id
      }).execute(function(response) {
        deferred.resolve(response)
      });

      deferred.promise.then(function(response) {
        $scope.tournament = response;
        $scope.setLoading(false);
      });
    };

    $scope.startTimer = function() {
      return $interval(function() {
        if ($scope.tournament && $scope.tournament.status > 1) {
          var round_duration = $scope.tournament.round_duration;
          var time_remaining = parseInt(round_duration) * 60000;
          if ($scope.tournament.current_round.start_date) {
            var start_time = new Date($scope.tournament.current_round.start_date).getTime();
            var current_time = new Date().getTime();

            time_remaining += start_time - current_time;

            if (time_remaining < 0) {
              time_remaining = 0
            }

          }
          time_remaining = Math.floor(time_remaining/1000);
          var seconds = time_remaining % 60;
          if (seconds < 10) {
            seconds = '0' + seconds;
          }

          var minutes = Math.floor(time_remaining/60);
          if (minutes < 10) {
            minutes = '0' + minutes;
          }

          $scope.timer = minutes + ':' + seconds;
        } else {
          $scope.timer = null;
        }
      }, 1000);
    }

    $scope.startPooling = function() {
      return $interval(function() {
        if ($scope.tournament && $scope.tournament.status > 1) {
          $scope.loadTournament($routeParams.tournament_id);
        }
      }, 10000)
    }

    $scope.subscribe = function() {
      if ($scope.tournament) {
        var deferred = $q.defer();

        $scope.setLoading(true);
        gapi.client.request({
          'root': apisRoot,
          'path': '/duels/v1/tournament/' +
            $scope.tournament.tournament_id + '/subscribe'
        }).execute(function(response) {
          deferred.resolve(response)
        });

        deferred.promise.then(function(response) {
          $scope.tournament = response;
          $scope.setLoading(false);
        });
      }
    }

    $scope.$watch(
      'ready',
      function(newValue, oldValue) {
        if (newValue) {
          $scope.loadTournament($routeParams.tournament_id);
        }
      }
    )

    $scope.$watch(
      'tournament.current_round',
      function(newValue, oldValue) {
        if (newValue && $scope.tournament.status < 5) {
          if (!$scope.startedInterval) {
            $scope.timerInterval = $scope.startTimer();
            $scope.poolingInterval = $scope.startPooling();
            $scope.startedInterval = true;
          }
        } else {
          $interval.cancel($scope.timerInterval);
          $scope.timerInterval = undefined;
          $interval.cancel($scope.poolingInterval);
          $scope.poolingInterval = undefined;
          $scope.startedInterval = false;
        }
      }
    )

    $scope.$on('$destroy', function() {
      if ($scope.timer) {
        $interval.cancel($scope.timerInterval);
        $interval.cancel($scope.poolingInterval);
      }
    });

    $scope.toggleTournamentDetails = function() {
      $scope.isDetailsDisplayed = !$scope.isDetailsDisplayed;
    }
  }
]).controller('tournamentsListCtrl', ['$scope', '$q',
  function($scope, $q) {
    $scope.loadTournaments = function() {
      var deferred = $q.defer();

      $scope.setLoading(true);

      gapi.client.request({
        'path': '/duels/v1/tournament',
        'root': apisRoot
      }).execute(function(response){
        deferred.resolve(response);
      });

      deferred.promise.then(function(response) {
        $scope.tournaments = response.tournaments;
        $scope.setLoading(false);
      })
    };

    $scope.$watch(
      'ready',
      function(newValue, oldValue) {
        if (newValue) {
          $scope.loadTournaments();
        }
      }
    );
  }
]);
