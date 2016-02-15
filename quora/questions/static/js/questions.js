$(function () {
  $(".publish").click(function () {
    $("input[name='status']").val("P");
    $("form").submit();
  });

  $(".draft").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });

  $(".answer").click(function () {
      $.ajax({
        url: '/questions/comment/',
        data: $("#comment-form").serialize(),
        cache: false,
        type: 'post',
        success: function (data) {
          $("#comment-list").html(data);
          var comment_count = $("#comment-list .comment").length;
          $(".comment-count").text(comment_count);
          $("#comment").val("");
          $("#comment").blur();
          $('#myModal').modal('hide');
          location.reload();
        },
        error: function () {
          window.location.assign("/login")
        }
      });
    });

  $(".vote").click(function () {
    var span = $(this);
    var comment = $(this).closest(".comment").attr("comment-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".comment")).val();
    var vote = "";
    if ($(this).hasClass("voted")) {
    }
    else {
    }
    $.ajax({
      url: '/questions/vote/',
      data: {
        'comment': comment,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        var options = $(span).closest('.options');
        data = JSON.parse(data)
        if (data.highlight == true) {
          $('.vote', options).addClass('voted');
        } else {
          $('.vote', options).removeClass('voted');
        }
        $('.votes', options).text(data.upvotes);
      },
      error: function () {
        window.location.assign("/login")
      }
    });
  });

});
