runserver:
	DEBUG="true" python ./manage.py runserver

test:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --reuse-db --cov-report term-missing --cov=core

test-watch:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s -f --reuse-db core/tests.py
