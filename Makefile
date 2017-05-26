runserver:
	DEBUG=True TEST_ENV=True python ./manage.py runserver

test-createdb:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --create-db

test:
	DEBUG=True TEST_ENV=True py.test -W ignore --ds=epracas.settings -s

test-watch:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s -f

test-coverage:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --cov-report term-missing

testw:
	DEBUG=True TEST_ENV=True py.test --ds=epracas.settings -s --create-db --ignore=env
