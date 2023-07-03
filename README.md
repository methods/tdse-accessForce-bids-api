# tdse-accessForce-bids-api
# API Documentation

This API provides an endpoint to post a new bid document.

## Prerequisites

- Python 3.x
- Flask
- Homebrew

## Running the API

1. Clone the repository to your local machine:

      ```bash
      git clone
      ```
2. Navigate to the root directory of the project:

      ```bash
      cd tdse-accessForce-bids-api
      ```
3. Install python 3.x if not already installed. You can check if it is installed by running the following command:

      ```bash
      python3 --version
      ```
4. Create the virtual environment by running the following command:

      ```
      python3 -m venv .venv
      ```
5. Run the virtual environment by running the following command:

      ```bash
      source .venv/bin/activate
      ``` 
6. Install the required dependencies by running the following command:

      ```bash
      pip install -r requirements.txt
      ```
7. Run the following command to start the API:

      ```bash
      python app/app.py
      ```
8. The API will be available at http://localhost:8080/api/bids

--------------

## Accessing API Documentation (Swagger Specification)

1. Run the following command to start the API:

      ```bash
      python app/app.py
      ```
2. The Swagger Specification will be available at http://localhost:8080/api/docs


--------------

## Installing and running an instance of MongoDB on your local machine (MacOS)

### To install on Windows please see [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)

1. Install Homebrew if not already installed. You can check if it is installed by running the following command:

      ```bash
      brew --version
      ```
2. Install MongoDB by running the following commands:

      ```bash
      brew tap mongodb/brew
      brew install mongodb-community
      ```
3. To run MongoDB (i.e. the mongod process) as a macOS service, run:

      ```bash
      brew services start mongodb-community@6.0
      ```
4. Run the following command to stop the MongoDB instance, as needed:

      ```bash
      brew services stop mongodb-community@6.0
      ```
5. To verify that MongoDB is running, run:

      ```bash
      brew services list
      ```
   You should see the service `mongodb-community` listed as `started`.

6. To begin using MongoDB, connect mongosh to the running instance. From a new terminal, issue the following:

      ```bash
      mongosh
      ```
7. To exit the MongoDB shell, run the following command:

      ```bash
      exit
      ``` 
OPTIONAL - Download MongoDB Compass to view the database in a GUI. You can download it from [here](https://www.mongodb.com/try/download/compass)

--------------

### Contributing to this project

See [CONTRIBUTING](https://github.com/methods/tdse-accessForce-bids-api/blob/main/CONTRIBUTING.md) for details

### License

See [LICENSE](https://github.com/methods/tdse-accessForce-bids-api/blob/main/LICENSE.md) for details
