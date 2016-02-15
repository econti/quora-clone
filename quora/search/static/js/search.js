$(function () {
  $(".feed-results li").click(function () {
    var feed = $(this).attr("feed-id");
    location.href = "/feeds/" + feed + "/";
  });

  $(".questions-results li").click(function () {
    var question = $(this).attr("question-slug");
    location.href = "/questions/" + question + "/";
  });

  $(".questions-results li").click(function () {
    var question = $(this).attr("question-id");
    location.href = "/questions/" + question + "/";
  });

});
