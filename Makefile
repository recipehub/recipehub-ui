test:
	foreman run python manage.py test

test_verbose:
	foreman run python manage.py test -v 2

test_api:
	foreman run python manage.py test ui.recipehub.tests.test_api

bower:
	cd ui/static && bower install
