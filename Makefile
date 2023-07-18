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

clean:
	rm -rf __pycache__
	rm -rf .venv
	rm -rf .pytest_cache
