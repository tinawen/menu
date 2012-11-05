// Generated by CoffeeScript 1.4.0
(function() {
  var _this = this;

  $('.picker').on("click", function() {
    return $('.nav').toggleClassName('display');
  });

  $(document).on("keyup", function(e) {
    if (e.which === 27) {
      $('.modal').removeClassName('display');
      $('.modal-wrap').removeClassName('display');
      return $('.nav').removeClassName('display');
    }
  });

  $('#submit-feedback').on("click", function() {
    $('.feedback-form').toggleClassName('display');
    return $('.feedbackf').toggleClassName('display');
  });

  $('.cancel').on("click", function() {
    $('.feedback-form').toggleClassName('display');
    return $('.feedbackf').toggleClassName('display');
  });

}).call(this);
