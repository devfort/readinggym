JS.Test.describe("Speed", function() { with(this) {
  before(function() {
    $("#fixture").html('\
      <div class="timer">\
        <p class="explanation"></p>\
        <div id="timer-control"></div>\
        <form>\
          <input type="hidden" name="seconds">\
        </form>\
      </div>')

    enhanceTimerModule(".timer", "Explanation")
    this.timer = $(".timer")
  })

  after(function() {
    $("#fixture").empty()
  })

  it("injects some buttons", function() { with(this) {
    assertEqual( 1, timer.find("button.start").length )
    assertEqual( 1, timer.find("button.next").length )
  }})

  describe("when the button is clicked", function() { with(this) {
    before(function() { with(this) {
      this.button = timer.find("button.start")
      button.click()
    }})

    it("changes to a stop button", function() { with(this) {
      assertEqual( "Done", button.text() )
    }})

    describe("again", function() { with(this) {
      before(function() { with(this) {
        this.form = timer.find('form')[0]
        stub(form, "submit")
      }})

      it("populates the 'seconds' field", function() { with(this) {
        button.click()
        assertMatch( /^[0-9.]+$/, timer.find("[name=seconds]").val() )
      }})

      it("submits the form", function() { with(this) {
        expect(form, "submit")
        button.click()
      }})
    }})
  }})
}})
