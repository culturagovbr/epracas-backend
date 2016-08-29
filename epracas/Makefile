runserver:
	DEBUG="true" python ./manage.py runserver

test:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --create-db

test-reusedb:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --reuse-db

test-watch:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s -f --reuse-db

test-coverage:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --reuse-db --cov-report term-missing
