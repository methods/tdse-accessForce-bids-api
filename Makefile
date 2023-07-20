.ONESHELL:

.DEFAULT_GOAL := run
TOPICS := fix - feat - docs - style - refactor - test - chore - build


PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip


.PHONY: run test clean check help commit swagger format branch lint

venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./.venv/bin/activate

run: venv
	$(PYTHON) app.py

test: venv
	coverage run -m pytest -vv
	@echo "TEST COVERAGE REPORT"
	coverage report -m --omit="tests/*"

branch:
	@echo "Available branch types:"
	@echo "$(TOPICS)"
	@read -p "Enter the branch type: " type; \
	read -p "Enter the branch description (kebab-case): " description; \
	git checkout -b $${type}/$${description}; \
	git push --set-upstream origin $${type}/$${description}

commit: format
	@echo "Available topics:"
	@echo "$(TOPICS)"
	@read -p "Enter the topic for the commit: " topic; \
	read -p "Enter the commit message: " message; \
	git add .; \
	git commit -m "$${topic}: $${message}"; \
	git push

check: venv
	$(PIP) install safety
	$(PIP) freeze | $(PYTHON) -m safety check --stdin

clean:
	@echo "Cleaning up..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name ".pytest_cache" -exec rm -rf {} +
	@find . -name ".venv" -exec rm -rf {} +

lint: venv
	$(PIP) install flake8 pylint
	$(PYTHON) -m flake8 
	$(PYTHON) -m pylint **/*.py

format: 
	$(PIP) install black
	$(PYTHON) -m black .

help:
	@echo "gmake run - run the application"
	@echo "gmake test - run the tests"
	@echo "gmake clean - remove all generated files"
	@echo "gmake check - check for security vulnerabilities"
	@echo "gmake branch - create and checkout to new branch"
	@echo "gmake commit - commit changes to git"
	@echo "gmake lint - run linters"
	@echo "gmake format - format all files in directory"
	@echo "gmake help - display this help"

swagger: venv
	open http://localhost:8080/api/docs/#/
	$(PYTHON) app.py