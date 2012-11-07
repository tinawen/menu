layout= ->
  count = $('.dish').length

  switch count
    when 1 then font_size = "40px"
    when 2, 3, 4 then font_size = "30px"
    when 5, 6, 7, 8, 9 then font_size = "22px"
    else font_size = "18px"

  $("body").css "font-size", font_size

  #insert breakpoints
  all_breakpoints = [[], [], [2], [3], [3], [4], [3, 5], [3, 6], [4, 7], [4, 7]]
  breakpoints = all_breakpoints[count-1];

  for breakpoint in breakpoints
    $('.dish').eq(breakpoint-1).before '<li class="break"></li>'
  return

$ ->
  setInterval "location.reload(true)", 180000
  layout()

