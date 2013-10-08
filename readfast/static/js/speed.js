'use strict';

var enhanceTimerModule = function(explanation) {
    var $timing = $('<button>Start</button>');
    
    $timing.one("click", function() {
        var t = Date.now();
        $timing.one("click", function() {
            t = Date.now() - t;
            $('#timer-module input[name="seconds"]').val(t / 1000);
            $('#timer-module form').submit();
        }).text("Done");
    });

    $('#timer-module #timer-control').html($timing);
    $('#timer-module .explanation').html(explanation);
    $('#timer-module').addClass('enhanced');
};
