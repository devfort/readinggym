JS.Test.describe("Regulator", function() { with(this) {
  before(function() {
    $("#fixture").html('\
      <div class="article">\
        <span>This</span> <span>is</span> <span>SPACE</span><br>\
        <span>It</span> <span>is</span> <span>kinda</span> <span>quiet</span>\
      </div>')

    this.pager = {firstPage: function() {}}
    this.regulator = new Regulator(".article", this.pager, 200)
  })

  after(function() {
    $("#fixture").empty()
  })

  it("counts the lines", function() { with(this) {
    assertEqual( 2, regulator.lines.length )
  }})

  it("records the words in the lines", function() { with(this) {
    var words = $.map(regulator.lines, function(line) {
      return {
        words: $.map(line.words, function(word) { return word.text() })
      }
    })
    assertEqual( [
        {words: ["This", "is", "SPACE"]},
        {words: ["It", "is", "kinda", "quiet"]}
      ], words )
  }})
}})
