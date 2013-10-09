function Pager(article) {
    this.article = $(article);
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

    $("#current-page").text(this.currentPage());
    $("#page-count").text(this.pages());
};

Pager.prototype.currentPage = function () {
    return -Math.round(
        (parseInt(this.contentBox.css("margin-top")) / this.article.height())
        - 0.5
    ) + 1; 
};

Pager.prototype.pages = function () {
    return Math.round((this.contentBox.height() / this.article.height()) + 0.5);
};

Pager.prototype.firstPage = function (callback) {
    this.contentBox.transition({
        "margin-top": "0"
    }, 100, $.proxy(function () {
        $("#current-page").text(this.currentPage());
        if(callback) callback();
    }, this));
};

Pager.prototype.isLastPage = function (callback) {
    return (
        -(parseInt(this.contentBox.css("margin-top")) - this.article.height()) >=
        this.contentBox.height()
    ) 
};

Pager.prototype.nextPage = function (callback) {
    if(!this.isLastPage()) {
        this.contentBox.transition({
            "margin-top": "-=" + this.article.height(),
        }, 100, $.proxy(function() {
            $("#current-page").text(this.currentPage());
            if(callback) callback();
        }, this));
    }
};

function Regulator(article, pager, wpm) {
    this.article = $(article);
    this.pager = pager;
    this.wpm = wpm;
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

    this.pager.firstPage();

    this.box = $("<div>").addClass("regulator").hide();
    $("article").append(this.box);

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

    var box = this.box;
    var lines = this.lines;
    var words = this.article.find("span");

    var wordsPerLine = words.length / lines.length;
    var pixelsPerWord = this.article.width() / wordsPerLine;
    
    var guideWidth = 6;
    var lineNo = 0;

    var guideLine = function () {
        if(lineNo == lines.length) { self.finish(); return; }
        if(!self.running) { return; }

        var line = lines[lineNo];
        var firstWordPos = line.words[0].position();
        var lineLeft = firstWordPos.left;
        var lineBottom = firstWordPos.top + line.words[0].height();
        var pixelRate = (self.wpm / 60) * pixelsPerWord;
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

            if (self.wpm < 1000) {
                box.transition({
                    left: lineLeft,
                    top: lineBottom,
                    width: guideWidth
                }, 0).show().position();

                box.transition({
                    left: (lineLeft + line.width) - guideWidth,
                }, guideTime, 'linear', function () {
                    lineNo += 1;
                    box.hide();
                    box.delay(100).queue(function() {
                        guideLine();
                        $(this).dequeue();
                    });
                }).position();
            } else {
                setTimeout(function () {
                    lineNo += 1;
                    guideLine();
                }, guideTime + 100);
            }
        };

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
    this.box.hide();
};

Regulator.prototype.finish = function() {
    $("#proceed").show();
    this.stop();
}


if (!$.support.transition)
    $.fn.transition = $.fn.animate;

