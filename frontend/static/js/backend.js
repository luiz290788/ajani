$(document).ready(function() {
  $('a.remove-btn').click(function() {
    $('input[name=user-id]').val($(this).attr('userId'));
    $('#remove-user').click();
  });

  $('a.delete-tournament-link').click(function() {
    if (confirm('Do you really want to delete this tournament?')) {
      $('form#delete-tournament-form input[name=tournament-key]').val($(this).attr('id'));
      $('#delete-tournament-btn').click();
    }
  });

  $('.user').click(function() {
  	if (!$(this).hasClass('active')) {
      activate_user($(this));
    }
    else {
      desactivate_user($(this))
    }
  })

  check_duplicate_match();

  function activate_user(element) {
    var user_id = get_user_id(element);

    $('.user').removeClass('active');
    $('.user').removeClass('selected');
    $('.match').removeClass('active');

    $(element).addClass('selected');
    $('.user-' + user_id).addClass('active');
    $('.user-' + user_id).parent().addClass('active');
  }

  function desactivate_user(element) {
    $('.user').removeClass('active');
    $('.user').removeClass('selected');
    $('.match').removeClass('active');
  }

  function get_user_id(element) {
    var class_list = element[0].className.split(/\s+/);
    for (var i = 0; i < class_list.length; i++) {
      if (class_list[i].search('user-') === 0) {
        return class_list[i].replace('user-', '');
      }
    }
    return false;
  }

  function check_duplicate_match() {
    $('#participants td').each(function() {
      var user_1_id = $(this).attr('id');
      $(this).addClass('checked');
      $('#participants td:not(.checked)').each(function() {
        var user_2_id = $(this).attr('id');
        var matches_count = 0;
        $('.round .user-' + user_1_id).each(function() {
          if ($(this).siblings('.user-' + user_2_id).length) {
            matches_count++;
          }
        });
        if (matches_count >= 2) {
          var name_1 = $('#participants #' + user_1_id).text();
          var name_2 = $('#participants #' + user_2_id).text();
          $('.round .user-' + user_1_id).siblings('.user-' + user_2_id).parent().addClass('duplicated');
          $('.round .user-' + user_2_id).siblings('.user-' + user_1_id).parent().addClass('duplicated');
          alert('Duplicate match detected between ' + name_1 + ' and ' + name_2);
        }
      });
    });
  }
})
