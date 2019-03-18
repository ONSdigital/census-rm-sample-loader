build:
	pipenv install --dev

lint:
	pipenv run flake8 . ./tests
	pipenv check . ./tests

test: lint
	pipenv run pytest --cov-report term-missing --cov . --capture no

docker: test
	docker build -t eu.gcr.io/census-rm-ci/census-rm-sample-loader .
