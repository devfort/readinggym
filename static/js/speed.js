'use strict';


var enhanceTimerModule = function(timerModule, explanation, pager) {
    var $timerModule        = $(timerModule),
        $timerButton        = $('<button>Start</button>').attr("id", "control-article"),
        startInMillis       = 0,
        finshInMillis       = 0,
        elapsedTimeInMillis = 0,
        checkForLastPage    = function() {
            if (pager.isLastPage()) {
               $timerButton.text("Done");
            }
        };
    
    $timerButton.click(function() {
        var buttonText = $timerButton.text();
        if (/start/i.test(buttonText)) {
            startInMillis = Date.now();
            $timerButton.text("Page Down");
        }

        if (/page down/i.test(buttonText)) {
            pager.nextPage(checkForLastPage);
        }

        if (/done/i.test(buttonText)) {
            finshInMillis = Date.now();
            elapsedTimeInMillis = finshInMillis - startInMillis;
            $timerModule.find('input[name="seconds"]').val(elapsedTimeInMillis / 1000);
            $timerModule.find('form').submit();
        }
    });

    $timerModule.find('#timer-control').html($timerButton);
    $timerModule.find('.explanation').html(explanation);
    $timerModule.addClass('enhanced');

};
