.PHONY: install pre-build build black pycodestyle

## @CI_actions Installs the checked out version of the code to your poetry managed venv
install:
	poetry install

## @CI_actions Runs code quality checks
pre-build: black unit-tests
	rm setup.py || echo "There was no setup.py"
	poetry show --no-dev | awk '{print "poetry add "$$1"=="$$2}' | sort | sh

## @CI_actions Builds the project into an sdist
build:
	poetry build -f sdist

## @Code_quality Runs black on the checked out code
black:
	poetry run black uk_bin_collection

## @Code_quality Runs pycodestyle on the the checked out code
pycodestyle:
	poetry run pycodestyle --statistics -qq uk_bin_collection

## @Testing runs unit tests
tests: ## runs tests for the project
	poetry run coverage run --omit "*/tests/*" -m pytest -n $(cpus) --alluredir=build/$(matrix)/allure-results
	poetry run coverage xml
