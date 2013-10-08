function Regulator(article) {
    this.article = article;
    this.setup();
    this.running = false;
}

Regulator.prototype.setup = function() {
    var spans = this.article.find("span");
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

    this.lines = lines;
};

Regulator.prototype.start = function() {
    this.running = true;
    this.article.addClass('reading');
    var box = $("<div>").addClass("regulator");
    $("body").append(box);

    var lines = this.lines;
    var regulator = this;
    var guideWidth = 6;
    var pixelRate = 200;
    var lineNo = 0;
    var guideLine = function () {
        if(!regulator.running) { return; }
        var line = lines[lineNo];
        var guideTime = ((line.width - guideWidth) / pixelRate)* 1000;
        
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

        regulator.animation = box.animate({
            left: (line.left + line.width) - guideWidth,
        }, guideTime, 'linear', function () {
            lineNo += 1;
            box.hide();
            regulator.nextTick = window.setTimeout(guideLine, 100);
        });
    };

    guideLine();
};

Regulator.prototype.stop = function() {
    this.article.removeClass('reading');
    this.article.find('span.highlight').removeClass('highlight');
    this.running = false;
    if(this.nextTick) {
        window.clearTimeout(this.nextTick);
    }
    if(this.animation) {
        this.animation.finish();
    }
}


$(function() {
  var regulator = new Regulator($("article"));

  $('#practice').click(function() {
    if(regulator.running) {
      regulator.stop();
      $(this).text('Start');
    } else {
      regulator.start();
      $(this).text('Stop');
    }
  });

  $("#practice").focus();
});

