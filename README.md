# tdse-accessForce-bids-api
# API Documentation

This API stores and serves information about Methods bids for client tenders.

## Prerequisites

- Python 3.x
- Flask
- Homebrew
- Makefile

## Running the API

1. Run the following command to start the API:

      ```bash
      make run
      ```
 * The API will be available at http://localhost:8080/api/bids

2. To see all available Make targets, run the following command in a new terminal:

      ```bash
      make help
      ```
3. Follow this link to go to the authorization documentation: [Authorization Documentation](https://github.com/methods/tdse-accessForce-auth-stub/blob/main/README.md)

4. In a new terminal enter the following command to run authorization server if not already running. This will be needed to generate a token:

      ```bash
      make auth
      ```
 * The API will be available at http://localhost:5000/authorise

--------------

## Environmental Variables

In order to validate your credentials, configure the database connection and utilise pagination you will have to set up the environmental variables locally.

To do this, create a `.env` file in your root folder, with the following key/value pairs:

      API_KEY=THIS_IS_THE_API_KEY
      SECRET_KEY=THIS_IS_A_SECRET
      DB_HOST=localhost
      DB_NAME=bidsAPI
      TEST_DB_NAME=testAPI
      DEFAULT_OFFSET=0
      DEFAULT_LIMIT=20
      MAX_OFFSET=2000
      MAX_LIMIT=1000
      DEFAULT_SORT_BIDS=bid_date
      DEFAULT_SORT_QUESTIONS=description
      APP_NAME=BidsAPI
      APP_VERSION=0.8.0
      APP_LANG=Python    

--------------

## Installing and running an instance of MongoDB on your local machine (MacOS)

### To install on Windows please see [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)

1. Install MongoDB by running the following commands:

      ```bash
      brew tap mongodb/brew
      brew install mongodb-community
      ```
2. To run MongoDB (i.e. the mongod process) as a macOS service, run:

      ```bash
      make mongostart
      ```
3. To verify that MongoDB is running, run:

      ```bash
      brew services list
      ```
   You should see the service `mongodb-community` listed as `started`.
4. Run the following command to stop the MongoDB instance, as needed:

      ```bash
      make mongostop
      ```
5. To begin using MongoDB, connect the MongoDB shell (mongosh) to the running instance. From a new terminal, issue the following:

      ```bash
      mongosh
      ```
6. To create a new database called `bidsAPI`, run:

      ```bash
      use bidsAPI
      ```
7. To create a new test database called `testAPI`, run:

      ```bash
      use testAPI
      ```
8. To exit the MongoDB shell, run the following command:

      ```bash
      exit
      ``` 
OPTIONAL - Download MongoDB Compass to view the database in a GUI. You can download it from [here](https://www.mongodb.com/try/download/compass)

--------------

## Database Setup

To set up the application database, run the following command:

      ```bash
      make setup
      ```

This will perform the following steps:

1. Clean up the existing database
2. Populate the bids collection with dummy data
3. Populate the questions collection with dummy data, using existing bid IDs

--------------

## Accessing API Documentation (OAS)

1. Run the following command to start the API (if you haven't already):

      ```bash
      make run
      ```
2. In a new terminal run the following command to view the Swagger UI in your default web browser:
      
      ```bash
      make swag
      ```
--------------

## Testing the application

1. Follow the steps above to start the API, authorization server and database connection (if you haven't already).

2. Run the following command to setup the test database:

      ```bash
      make test-setup
      ```
3. Enter the following command to run the test suites and generate a test coverage report:
      
      ```bash
      make test
      ```
4. Enter the following command to run the integration tests:
      
      ```bash
      make test-integration
      ```
--------------

## Using auth playground to generate a token and make authenticated requests to the Bids API

1. Follow the steps above to start the API, authorization server and database connection (if you haven't already).

2. In a new terminal enter the following command to open the auth playground in your default web browser:

      ```bash
      make authplay
      ```
3. Follow the steps in the auth playground to generate a token and much more.

--------------

### Contributing to this project

See [CONTRIBUTING](https://github.com/methods/tdse-accessForce-bids-api/blob/main/CONTRIBUTING.md) for details

### License

See [LICENSE](https://github.com/methods/tdse-accessForce-bids-api/blob/main/LICENSE.md) for details
