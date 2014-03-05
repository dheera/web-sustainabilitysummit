$(document).ready(function(){
  $('.nodrag').mousedown(function(event){event.preventDefault();});
  $('.clickable').mouseenter(function(){$(this).addClass('clickable_hover');}).mouseleave(function(){$(this).removeClass('clickable_hover');}).mousedown(function(event){event.preventDefault();});
  $(".swipebox").swipebox();
});

var isHDDisplay = window.devicePixelRatio > 1;
var cssTransitionsSupported = false;
(function() {
    var div = document.createElement('div');
    div.innerHTML = '<div style="-webkit-transition:color 1s linear;-moz-transition:color 1s linear;"><\/div>';
    cssTransitionsSupported = (div.firstChild.style.webkitTransition !== undefined) || (div.firstChild.style.MozTransition !== undefined);
    delete div;
})();
