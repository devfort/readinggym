'use strict';

var enhanceTimerModule = function(timerModule, explanation, pager) {
  var $timerModule        = $(timerModule),
      $timerButton        = $('<button>Start</button>').attr("id", "control-article"),
      startInMillis       = 0,
      finshInMillis       = 0,
      elapsedTimeInMillis = 0;

  $timerButton.click(function() {
    var buttonText = $timerButton.text();

    if (/start/i.test(buttonText)) {
      startInMillis = new Date().getTime();
      $timerButton.text("Page Down");
    }

    if (/page down/i.test(buttonText)) {
      pager.nextPage(function() {
        if (pager.isLastPage()) $timerButton.text("Done");
      });
    }

    if (/done/i.test(buttonText)) {
      finshInMillis = new Date().getTime();
      elapsedTimeInMillis = finshInMillis - startInMillis;
      $timerModule.find('input[name="seconds"]').val(elapsedTimeInMillis / 1000);
      $timerModule.find('form').submit();
    }
  });

  $timerModule.find('#timer-control').html($timerButton);
  $timerModule.find('.explanation').html(explanation);
  $timerModule.addClass('enhanced');
};
