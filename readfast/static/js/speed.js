'use strict';

$(function () {
    $( '#timing' ).click(function() {
        var t = Date.now();
        $( '#timing').off().text('Stop');
        $( '#timing').click(function() {
            $( '#timing').remove();
            t = Date.now() - t;
            $('input[name="seconds"]').val(t / 1000);
            $('form').submit();
        });
    });
    $('.enhanced').show();
    $('.noscript').hide();
});
