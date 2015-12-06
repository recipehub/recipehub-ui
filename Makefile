test:
	foreman run python manage.py test

bower:
	cd ui/static && bower install
