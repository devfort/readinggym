$(function () {
    var spans = $("article span");

    var lines = [];
    var words = [];
    var lastOffset;
    var last$e;
    var first$e;
    var firstOffset;
    var widthSum = 0;

    spans.each(function (i, e) {
        var $e = $(e);
        var offset = $e.offset();

        // track the start of each line
        if(!first$e) {
            first$e = $e;
            firstOffset = offset;
        }
        
        if (offset && lastOffset) {
            if(offset.top != lastOffset.top) {
                lines.push({
                    left: firstOffset.left,
                    width: widthSum,
                    height: last$e.height(),
                    bottom: lastOffset.top + last$e.height(),
                    words: words
                });

                widthSum = 0;
                firstOffset = offset;
                first$e = $e;
                words = [];
            }
        }

        words.push(e);
        widthSum += $e.width();
        lastOffset = offset;
        last$e = $e;
    });

    var box = $("<div>").addClass("regulator");
    $("body").append(box);

    var guideWidth = 6;
    var pixelRate = 200;
    var lineNo = 0;
    var guideLine = function () {
        var line = lines[lineNo];
        var guideTime = ((line.width - guideWidth) / pixelRate)* 1000;
        console.log(line, lineNo, guideTime);
        
        $(line.words).each(function(i,s) {
          $(s).addClass('highlight');
        });
        if(lineNo > 0) {
          $(lines[lineNo-1].words).each(function(i,s) {
            $(s).removeClass('highlight');
          });
        }
        box.css({
            left: line.left,
            top: line.bottom,
            width: guideWidth
        });
        box.show();

        box.animate({
            left: (line.left + line.width) - guideWidth,
        }, guideTime, 'linear', function () {
            lineNo += 1;
            box.hide();
            window.setTimeout(guideLine, 100);
        });
    };

    guideLine();
});

