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

    this.pager = {
      isLastPage: function() {},
      nextPage:   function() {}
    }

    enhanceTimerModule(".timer", "Explanation", this.pager)
    this.timer = $(".timer")
    this.button = this.timer.find("button")
  })

  after(function() {
    $("#fixture").empty()
  })

  it("injects a start button", function() { with(this) {
    assertEqual( 1, button.length )
    assertEqual( "Start", button.text() )
  }})

  describe("when the button is clicked in a start state", function() { with(this) {
    before(function() { with(this) {
      button.click()
    }})

    it("changes to a next page button", function() { with(this) {
      assertEqual("Page Down", button.text() )
    }})
  }})

  describe("when the pager is on the last page", function() { with(this) {
    before(function() { with(this) {
      stub(pager, "isLastPage").returns(true)
      stub(pager, "nextPage").yields([])
    }})

    it("puts you in the 'page down' state if you click once", function() { with(this) {
      button.click()
      assertEqual( "Page Down", button.text() )
    }})

    it("puts you in the 'done' state if you click twice", function() { with(this) {
      button.click()
      button.click()
      assertEqual( "Done", button.text() )
    }})

    describe("and you've clicked twice", function() { with(this) {
      before(function() { with(this) {
        this.form = timer.find('form')[0]
        stub(form, "submit")
        button.click()
        button.click()
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
