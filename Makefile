test: pytest jstest

jstest:
	phantomjs static/tests/phantom.js

pytest:
	python manage.py test readfast assets
