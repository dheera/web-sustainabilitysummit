$(document).ready(function(){
  $('.nodrag').mousedown(function(event){event.preventDefault();});
  $('.clickable').mouseenter(function(){$(this).addClass('clickable_hover');}).mouseleave(function(){$(this).removeClass('clickable_hover');}).mousedown(function(event){event.preventDefault();});
});
