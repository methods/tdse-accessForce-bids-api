.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip


.PHONY: help auth clean mongostart mongostop run setup swag test

help:
	@echo "make help - display this help"
	@echo "make auth - run auth api application"
	@echo "make build - create and activate virtual environment"
	@echo "make clean - remove all generated files"
	@echo "make mongostart - start local mongodb instance"
	@echo "make mongostop - stop local mongodb instance"
	@echo "make run - run the application"
	@echo "make swag - open swagger documentation"
	@echo "make setup - setup the application database"
	@echo "make test - run tests and coverage report"
	@echo "make helptools - display help for tools"

auth:
	$(PYTHON) ../tdse-accessForce-auth-stub/app.py

build: requirements.txt
	python3 -m venv .venv
	$(PIP) install -r requirements.txt
	. ./.venv/bin/activate

clean:
	@echo "Cleaning up..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name ".pytest_cache" -exec rm -rf {} +
	@find . -name ".venv" -exec rm -rf {} +	

mongostart:
	@echo "Starting MongoDB..."
	brew services start mongodb-community@6.0

mongostop:
	@echo "Stopping MongoDB..."
	brew services stop mongodb-community@6.0

run: build
	$(PYTHON) app.py

setup:
	@echo "Setting up application database..."
	cd ./scripts/; \
	make dbclean; \
	make bids; \
	make questions
	@echo "Database setup complete."

swag:
	open http://localhost:8080/api/docs/#/

test: 
	-coverage run -m pytest -vv
	@echo "TEST COVERAGE REPORT"
	coverage report -m --omit="tests/*,dbconfig/*"


.PHONY: helptools authplay branch check commit format lint

helptools:
	make -f tools.mk help

authplay:
	cd ./scripts/; \
	make authplay

branch:
	make -f tools.mk branch

check:
	make -f tools.mk check

commit:
	make -f tools.mk commit

format: 
	make -f tools.mk format

lint:
	make -f tools.mk lint
