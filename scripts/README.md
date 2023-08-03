# MongoDB Database Cleanup and Sample Data Population Scripts

## Database Cleanup Script

### Script Description
- The delete_bids.py script is used to delete all bids from the MongoDB collection.
- The delete_questions.py script is used to delete all questions from the MongoDB collection.
- The create_bids.py script is used to populate the MongoDB database with sample bids data from the bids.json file.
- The create_questions.py script is used to populate the MongoDB database with sample questions data from the questions.json file, using existing bid Ids from the bids.json file.

### Usage

To run the database cleanup script, execute the following command:
```bash
make dbclean
```

Or to run the cleanup script for only the bids collection, execute:
```bash
python3 delete_bids.py
```

And to run the cleanup script for only the questions collection, execute:
```bash
python3 delete_questions.py
```

To run the sample bids data population script, execute the following command:
```bash
python3 create_bids.py
```

To run the sample questions data population script, execute the following command:
```bash
python3 create_questions.py
```
