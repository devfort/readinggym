# speedreader

A Django app for helping you read faster.

## Deploying

#apt

    apt-get install --yes python-virtualenv python-pip python-dev libpq-dev postgresql-9.1 nodejs npm

#Noooooooode setup

    npm install

#django setup

    python manage.py syncdb --migrate
    node_modules/.bin/wake

#server setup

    echo "Who can say?"

## Contributing

### Notes on static files

We use [`wake`](https://github.com/jcoglan/wake) to build static files for
production and [`wake_assets`](https://github.com/jcoglan/wake-assets-python) for
generating asset HTML. This means you will need [Node.js](http://nodejs.org/) to
run and deploy the app.

If any of the following is confusing, the above links point to copious
documentation.

We keep all static files in `./static` and the `wake` config is in
`package.json`. This is where you specify which JS/CSS files are in each bundle.
Always add files here and use `include_css`, `include_image` and `include_js` to
generate style/image/script tags rather than hand-writing them, so that the app
can dynamically generate links to source or optimised files.

`wake_assets` is configured using `WAKE_ASSETS` in `speedreader/settings.py`.
The glue that binds `wake_assets` into Django is in the `assets` app. You may
want to modify the middleware in `assets/__init__.py` to change the per-request
tag generation settings.

When you deploy the app, run this command to generate the optimised files:

```
$ ./node_modules/.bin/wake
```

and change `WAKE_ASSETS` to have `mode='targets'` and `cache=True`.


### JavaScript testing

We try to keep our JavaScript well-tested, using
[jstest](http://jstest.jcoglan.com). The tests are in `./static/tests`. To run
them, open this file (as a static file, not through the app):

```
$ open ./static/tests/browser.html
```

If you have [PhantomJS](http://phantomjs.org/) installed you can also run the
tests in the shell like this:

```
$ phantomjs ./static/tests/phantom.js
```


## License

The MIT License (MIT)

Copyright (c) 2013 /dev/fort 8

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
