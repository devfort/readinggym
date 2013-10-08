'use strict';

var enhanceTimerModule = function(explanation) {
var $timing = $('<button type="button">Start</button>');
$timing.click(function() {
  var t = Date.now();
  $timing
    .off()
    .text('Finish');
  $timing.click(function() {
    $timing.remove();
    t = Date.now() - t;
    $('#timer-module input[name="seconds"]').val(t / 1000);
    $('#timer-module form').submit();
  });
});
$('#timer-module #timer-control').html($timing);
$('#timer-module .explanation').html(explanation);
window.scrollTo(0, 0);
$('#timer-module').addClass('enhanced');
}