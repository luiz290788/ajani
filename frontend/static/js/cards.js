var cards = [];

header.directive('card', function() {
  return {
    link: function(scope, elm, attrs, ctrl) {
      if (!$(elm).hasClass('card')) {
        cards.push(elm);
        elm.addClass('card');
        scope.$on('$destroy', function() {
          cards.splice(cards.indexOf(elm), 1);
          updateCardsPosition();
        });
        scope.$watch(
          attrs.ngShow,
          updateCardsPosition
        )
        updateCardsPosition();
      }
    }
  };
});

function updateCardsPosition() {
  var columns = Math.round($('#cards-holder').width() / 250);

  var columnsSizes = [];
  for (var i = 0; i < columns; i++) {
    columnsSizes[i] = 0;
  }

  var columnSize = $('#cards-holder').width() / columns;

  angular.forEach(cards, function(card) {
    if ($(card).is(':visible')) {
      var minor = 0;
      for (var i in columnsSizes) {
        if (columnsSizes[minor] > columnsSizes[i]) {
          minor = i;
        }
      }
      $(card).css({
        '-webkit-transform': 'translate(' + (columnSize * minor) + 'px, ' + columnsSizes[minor] + 'px)',
        '-moz-transform': 'translate(' + (columnSize * minor) + 'px, ' + columnsSizes[minor] + 'px)',
        '-ms-transform': 'translate(' + (columnSize * minor) + 'px, ' + columnsSizes[minor] + 'px)',
        'width': (100 / columns - .5) + '%'
      })
      columnsSizes[minor] += $(card).outerHeight(true);
    }
  });
}

$(window).resize(updateCardsPosition);
