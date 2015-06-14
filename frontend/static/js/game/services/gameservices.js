(function(angular) {
  
  angular.module('wd.game')
    .factory('gameservices', gameservices);
  
  gameservices.$inject = ['$http'];
  
  function gameservices($http) {
    return {
      create: create,
      connect: connect,
      getState: getState,
      selectDeck: selectDeck,
      throwDice: throwDice,
      openHand: openHand,
      muligan: muligan,
      keep: keep,
      draw: draw,
      life: life,
      move: move,
      tap: tap,
      untap: untap,
      untapAll: untapAll,
      searchLibrary: searchLibrary,
      shuffle: shuffle,
      scry: scry,
      revealHand: revealHand,
      revealTop: revealTop,
      revealCard: revealCard
    };
    
    function revealCard(id, player, card) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'reveal_card',
        'card': card
      });
    }
    
    function revealTop(id, player, revealed) {
      if (revealed === undefined) {
        revealed = true;
      }
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'reveal_top',
        'top_revealed': revealed
      });
    }
    
    function revealHand(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'reveal_hand'
      });
    }
    
    function scry(id, player, options) {
      var event = angular.extend({'event': 'scry'}, options);
      return $http.post('/api/game/' + id + '/' + player, event);
    }
    
    function shuffle(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'shuffle'
      });
    }
    
    function searchLibrary(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'search_library'
      });
    }
    
    function untapAll(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'untap_all'
      });
    }
    
    function tap(id, player, card) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'tap',
        'card': card
      });
    }
    
    function untap(id, player, card) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'untap',
        'card': card
      });
    }
    
    function move(id, player, card, from, to, options) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'move',
        'card': card,
        'from': from,
        'to': to,
        'options': options
      });
    }
    
    function life(id, player, delta) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'life',
        'delta': delta
      });
    }
    
    function draw(id, player, count) {
      if (count === undefined) {
        count = 1
      }
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'draw',
        'count': count
      });
    }
    
    function play(id, player, card) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'play',
        'card': card
      });
    }
    
    function keep(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'keep'
      });
    }
    
    function muligan(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'muligan'
      });
    }
    
    function openHand(id, player) {
      return $http.get('/api/game/' + id + '/' + player + '/hand');
    }
    
    function throwDice(id, player) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'throw_dice'
      });
    }
    
    function selectDeck(id, player, deck) {
      return $http.post('/api/game/' + id + '/' + player, {
        'event': 'select_deck',
        'deck': parseInt(deck)
      });
    }
    
    function getState(id, player) {
      return $http.get('/api/game/' + id + '/' + player);
    }
    
    function create(kind) {
      return $http.post('/api/game/' + kind);
    }
    
    function connect(id) {
      return $http.put('/api/game/' + id);
    }
  };
  
})(angular);