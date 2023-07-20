.ONESHELL:

.DEFAULT_GOAL := run
TOPICS := fix - feat - docs - style - refactor - test - chore - build


PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip


.PHONY: run test clean check help commit swagger

venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./.venv/bin/activate

run: venv
	$(PYTHON) app.py

test: venv
	$(PYTHON) -m pytest

branch:
	@echo "Available branch types:"
	@echo "$(TOPICS)"
	@read -p "Enter the branch type: " type; \
	read -p "Enter the branch description: " description; \
	git checkout -b $${type}/$${description}; \
	git push --set-upstream origin $${type}/$${description}

commit:
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

help:
	@echo "gmake run - run the application"
	@echo "gmake test - run the tests"
	@echo "gmake clean - remove all generated files"
	@echo "gmake check - check for security vulnerabilities"
	@echo "gmake commit - commit changes to git"
	@echo "gmake help - display this help"

swagger: venv
	open http://localhost:8080/api/docs/#/
	$(PYTHON) app.py