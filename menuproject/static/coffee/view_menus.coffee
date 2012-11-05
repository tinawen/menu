$ ->
  $('.picker').click ->
    $('.nav').toggleClass 'display'

  $(document).on "keyup", (e) =>
    if e.which is 27
      $('.modal').removeClassName 'display'
      $('.modal-wrap').removeClassName 'display'
      $('.nav').removeClassName 'display'

  $('#submit-feedback').click ->
    $('.feedback-form').toggleClass 'display'
    $('.feedbackf').toggleClass 'display'

  $('.cancel').click ->
    $('.feedback-form').toggleClass 'display'
    $('.feedbackf').toggleClass 'display'

