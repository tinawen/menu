$ ->
  $("#datepicker").datepicker {
  dateFormat : 'yy-mm-dd'
  }

  $("form").submit ->
    $(@).submit ->
      return false
    return true

  $('#add-menu').click ->
    $('#add-menu-modal-wrap').addClass 'display'
    $('#add-menu-modal').addClass 'display'
    return

  $('.cancel').click ->
    $('#add-menu-modal-wrap').removeClass 'display'
    $('#add-menu-modal').removeClass 'display'
    return

