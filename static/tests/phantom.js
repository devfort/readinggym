phantom.injectJs('node_modules/jstest/jstest.js')

var reporter = new JS.Test.Reporters.Headless({})

reporter.open('static/tests/browser.html')
