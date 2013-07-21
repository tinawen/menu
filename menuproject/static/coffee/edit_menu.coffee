$ ->
  $("form").submit ->
    $(@).submit ->
      return false
    return true

  $('#add-menu-item').click ->
    $('#add-menu-item-modal').addClass "display"
    $('#add-menu-item-modal-wrap').addClass "display"
    return

  $('.cancel').click ->
    $('#add-menu-item-modal-wrap').removeClass 'display'
    $('#add-menu-item-modal').removeClass 'display'
    return

  $('.delete').click ->
    $.ajax
      type: "POST",
      url: "/delete_menu_item/" + $(this).attr("menu_item_id")
    .done (data) ->
      item_to_remove = $(".menu .dish").filter("#"+data).remove()

	$('#menuTitle').live 'change', ->
    $.ajax
      type: "POST",
      url: "/update_menu_name/" + $(this).attr("menu_id"),
      data: JSON.stringify(escape($(this).val())),
      contentType: 'application/json; charset=utf-8'
    .done (data) ->
       $('#menuTitle').val(JSON.parse data)

  $('.menu .dish-title').live 'change', ->
    $.ajax
      type: 'POST',
      url: "/update_menu_item_name/" + $(this)[0].getAttribute("menu_item_id"),
      data: JSON.stringify(escape($(this).val())),
      contentType: 'application/json; charset=utf-8'
    .done (data) ->
      $('#menuTitle').val(JSON.parse data)

  $('.menu .description').live 'change', ->
    $.ajax
      type: "POST",
      url: "/update_menu_item_desc/" + $(this)[0].getAttribute('menu_item_id'),
      data:JSON.stringify(escape($(this).val())),
      contentType: 'application/json; charset=utf8'

  $('.menu .checkbox#allergen').live 'change', ->
    data_name = if $(this).is(":checked") then "menu_item_allergen_on=" else "menu_item_allergen_off="
    $.ajax
      type:"POST",
      url: "/update_menu_item_allergen/" + $(this)[0].getAttribute('menu_item_id'),
      data:data_name + $(this)[0].getAttribute('allergenName')

  $('.menu .healthy-selection').live 'change', ->
    $.ajax
      type:"POST",
      url: "/update_menu_item_healthy/" + $(this)[0].getAttribute('menu_item_id'),
      data: "healthy=" + $(this).val()

  $ ->
    $("#sortable").sortable
      update: (event, ui) ->
        new_order = $(this).sortable('toArray').toString()
        menu_id = $(".menu ul").attr("menu_id")
        $.ajax
          type:"POST",
          url: "/update_menu_order/" + menu_id
          data:"menu_ids=" + new_order
    $("#sortable").disableSelection()

    $("#db-chooser").get(0).addEventListener "DbxChooserSuccess", (e) ->
      images = []
      for file in e.files
        images.push [file.link, file.thumbnails['64x64']]
      menu_id = $(".menu ul").attr("menu_id")

      $.ajax
        type: "POST"
        url: "/attach_pictures/" + menu_id
        data: "data=" + JSON.stringify(images)
      .success (data) ->
        data = JSON.parse data
        for thumb in data
          image_cell = $('<span />').addClass("image-cell")
          $('<div />').addClass("cancel").addClass("delete-thumb").appendTo image_cell
          $('<img />').attr("src", thumb).appendTo image_cell
          image_cell.appendTo $(".thumbs")

    $('.delete-thumb').click ->
      menu_id = $(".menu ul").attr("menu_id")
      img_url = $(this).next().attr("src")
      $.ajax
        type: "POST"
        url: "/delete_picture/" + menu_id
        data: "data=" + JSON.stringify(img_url)
      .success (data) ->
        thumb = $(".thumbs").find('img[src$="' + data + '"]')
        thumb.parent().remove()