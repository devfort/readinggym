function Pager(article) {
    this.article = article;
    this.setup();
}

Pager.prototype.setup = function () {
    var self = this;
    this.article.wrapInner("<div>");
    this.contentBox = this.article.find("div").first();
    this.article.css({
        "overflow": "hidden",
        "height": "30em"
    });
};

Pager.prototype.firstPage = function (cb) {
    this.contentBox.animate({
        "margin-top": "0",
    }, 100, cb);
}

Pager.prototype.nextPage = function (cb) {
    this.contentBox.animate({
        "margin-top": "-=" + this.article.height(),
    }, 100, cb);
};

function Regulator(article, pager) {
    this.article = article;
    this.pager = pager;
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
                    width: widthSum,
                    words: words
                });

                widthSum = 0;
                firstOffset = offset;
                first$e = $e;
                words = [];
            }
        }

        words.push($e);
        widthSum += $e.width();
        lastOffset = offset;
        last$e = $e;
    });

    lines.push({
        width: widthSum,
        words: words
    });

    this.lines = lines;
};

Regulator.prototype.start = function() {
    var self = this;

    this.running = true;
    this.article.addClass('reading');
    var box = $("<div>").addClass("regulator");
    $("article").append(box);

    var lines = this.lines;
    var words = this.article.find("span");
    var regulator = this;

    var wordsPerLine = words.length / lines.length;
    var pixelsPerWord = this.article.width() / wordsPerLine;
    var wpm = 500;
    
    var guideWidth = 6;
    var pixelRate = (wpm/60)*pixelsPerWord;
    var lineNo = 0;

    var guideLine = function () {
        if(lineNo == lines.length) { self.stop(); return }
        if(!regulator.running) { return; }

        var line = lines[lineNo];
        var firstWordPos = line.words[0].position();
        var lineLeft = firstWordPos.left;
        var lineBottom = firstWordPos.top + line.words[0].height();

        var guideTime = ((line.width - guideWidth) / pixelRate) * 1000;
        
        var animateGuide = function () {
            var firstWordPos = line.words[0].position();
            var lineBottom = firstWordPos.top + line.words[0].height();

            $(line.words).each(function(i,s) {
                $(s).addClass('highlight');
            });
        
            if(lineNo > 0) {
                $(lines[lineNo-1].words).each(function(i,s) {
                    $(s).removeClass('highlight');
                });
            }

            box.css({
                left: lineLeft,
                top: lineBottom,
                width: guideWidth
            }).show();

            regulator.animation = box.animate({
                left: (lineLeft + line.width) - guideWidth,
            }, guideTime, 'linear', function () {
                lineNo += 1;
                box.hide();
                regulator.nextTick = window.setTimeout(guideLine, 200);
            });
        }

        if(lineBottom > self.article.height()) {
            self.pager.nextPage(animateGuide);
        } else {
            animateGuide();
        }
    };

    this.pager.firstPage(guideLine);
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
    this.pager.firstPage();
}


$(function() {
  var pager = new Pager($("article"));
  var regulator = new Regulator($("article"), pager);

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

