.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip

venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./.venv/bin/activate

run: venv
	$(PYTHON) app.py

test: venv
	$(PYTHON) -m pytest

# security vulnerability checker
check:
	$(PIP) install safety
	$(PIP) freeze | $(PYTHON) -m safety check --stdin

clean:
	rm -rf __pycache__
	rm -rf .venv
	rm -rf .pytest_cache

help:
	@echo "make run - run the application"
	@echo "make test - run the tests"
	@echo "make clean - remove all generated files"
	@echo "make check - check for security vulnerabilities"
	@echo "make help - display this help"