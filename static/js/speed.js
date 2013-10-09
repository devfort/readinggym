'use strict';

var makeNextPageButton = function(article) {
    var pager = new Pager(article);
    var nextPageButton = $('<button class="next">Next page</button>');
    nextPageButton.click(function () {
        pager.nextPage();
    });
    return nextPageButton;
};

var enhanceTimerModule = function(timerModule, explanation) {
    timerModule = $(timerModule);
    var $timing = $('<button class="start">Start</button>');
    
    $timing.one("click", function() {
        var t = Date.now();
        $timing.one("click", function() {
            t = Date.now() - t;
            timerModule.find('input[name="seconds"]').val(t / 1000);
            timerModule.find('form').submit();
        }).text("Done");
    });

    timerModule.find('#timer-control').html($timing);
    timerModule.find('.explanation').html(explanation);
    timerModule.addClass('enhanced');

    $timing.before(makeNextPageButton($("article")));
};
