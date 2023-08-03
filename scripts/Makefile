.ONESHELL:

.PHONY: help authplay bids dbclean questions

help:
	@echo "make help - display this help"
	@echo "make authplay - get JWT and interact with auth api"
	@echo "make bids - populate bids collection"
	@echo "make dbclean - clean up the application database"
	@echo "make questions - populate questions collection"

authplay:
	@echo "Getting JWT..."
	@find . -name "get_jwt.py" -exec python3 {} \;

bids:
	@echo "Creating bids..."
	@find . -name "create_bids.py" -exec python3 {} \;

dbclean:
	@echo "Cleaning up database..."
	@find . -name "delete_bids.py" -exec python3 {} \;
	@find . -name "delete_questions.py" -exec python3 {} \;

questions:
	@echo "Creating questions..."
	@find . -name "create_questions.py" -exec python3 {} \;