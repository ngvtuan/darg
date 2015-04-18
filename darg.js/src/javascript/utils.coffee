# making table rows clickable
$('.table tr').each ->
  $(this).css('cursor', 'pointer').hover((->
    $(this).addClass 'active'
    return
  ), ->
    $(this).removeClass 'active'
    return
  )
  return
return
