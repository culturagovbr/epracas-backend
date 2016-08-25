runserver:
	DEBUG="true" python ./manage.py runserver

test:
	py.test --ds=epracas.settings -s --reuse-db --cov-report term-missing --cov=core
