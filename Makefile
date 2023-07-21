.ONESHELL:

.DEFAULT_GOAL := run
TOPICS := fix - feat - docs - style - refactor - test - chore - build


PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip


.PHONY: run test clean check help commit swagger format branch lint setup bids dbclean

help:
	@echo "gmake help - display this help"
	@echo "gmake bids - create sample data"
	@echo "gmake branch - create a new branch"
	@echo "gmake build - create and activate virtual environment"
	@echo "gmake check - check for security vulnerabilities"
	@echo "gmake clean - remove all generated files"
	@echo "gmake commit - commit changes to git"
	@echo "gmake dbclean - clean up the application database"
	@echo "gmake format - format the code"
	@echo "gmake lint - run linters"
	@echo "gmake run - run the application"
	@echo "gmake swagger - open swagger documentation"
	@echo "gmake setup - setup the application database"
	@echo "gmake test - run the tests"

bids:
	@echo "Creating sample data..."
	@find . -name "create_sample_data.py" -exec python3 {} \;

branch:
	@echo "Available branch types:"
	@echo "$(TOPICS)"
	@read -p "Enter the branch type: " type; \
	read -p "Enter the branch description (kebab-case): " description; \
	git checkout -b $${type}/$${description}; \
	git push --set-upstream origin $${type}/$${description}

build: venv/bin/activate
	. ./.venv/bin/activate

check:
	$(PIP) install safety
	$(PIP) freeze | $(PYTHON) -m safety check --stdin

clean:
	@echo "Cleaning up..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name ".pytest_cache" -exec rm -rf {} +
	@find . -name ".venv" -exec rm -rf {} +	

commit: format
	@echo "Available topics:"
	@echo "$(TOPICS)"
	@read -p "Enter the topic for the commit: " topic; \
	read -p "Enter the commit message: " message; \
	git add .; \
	git commit -m "$${topic}: $${message}"; \
	git push

dbclean:
	@echo "Cleaning up database..."
	@find . -name "delete_db.py" -exec python3 {} \;

format: 
	$(PIP) install black
	$(PYTHON) -m black .

lint:
	$(PIP) install flake8 pylint
	$(PYTHON) -m flake8 
	$(PYTHON) -m pylint **/*.py

run: build
	$(PYTHON) app.py

setup: build dbclean bids
	@echo "Setting up the application database..."

swag:
	open http://localhost:8080/api/docs/#/

test: test_setup
	coverage run -m pytest -vv
	@echo "TEST COVERAGE REPORT"
	coverage report -m --omit="tests/*,dbconfig/*"

test_setup: test_requirements.txt
	$(PIP) install -r test_requirements.txt

venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

