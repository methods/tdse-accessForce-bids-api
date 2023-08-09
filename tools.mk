.ONESHELL:

TOPICS := fix - feat - docs - style - refactor - test - chore - build

PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip

.PHONY: help branch check commit format lint

help:
	@echo "make helptools - display this help"
	@echo "make branch - create a new branch"
	@echo "make check - check for security vulnerabilities"
	@echo "make commit - commit changes to git"
	@echo "make format - format the code"
	@echo "make lint - run linters"

branch:
	@echo "Available branch types:"
	@echo "$(TOPICS)"
	@read -p "Enter the branch type: " type; \
	read -p "Enter the branch description (kebab-case): " description; \
	git checkout -b $${type}/$${description}; \
	git push --set-upstream origin $${type}/$${description}

check:
	$(PIP) install safety
	$(PIP) freeze | $(PYTHON) -m safety check --stdin

commit: format
	@echo "Available topics:"
	@echo "$(TOPICS)"
	@read -p "Enter the topic for the commit: " topic; \
	read -p "Enter the commit message: " message; \
	git add .; \
	git commit -m "$${topic}: $${message}"; \
	git push

format: 
	$(PYTHON) -m black .

lint:
	$(PYTHON) -m flake8 
	$(PYTHON) -m pylint **/*.py **/**/*.py *.py