# MongoDB Database Cleanup and Sample Data Population Scripts

## Database Cleanup Script

### Script Description
- The delete_db.py script is used to delete all bids from the MongoDB collection.
- The create_sample_data.py script is used to populate the MongoDB database with sample bids data from the bids.json file.

### Usage

To run the database cleanup script, execute the following command:
```bash
python3 delete_db.py
```

To run the sample data population script, execute the following command:
```bash
python3 create_sample_data.py
```

## Application Setup

### Script Description
The setup target in the Makefile sets up the application database by performing the following steps:

1. Building the application using the build target.
2. Cleaning up the existing database using the dbclean target.
3. Creating sample data using the bids target.

### Usage
To set up the application database, run the following command:
```bash
make setup
```