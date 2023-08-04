# tdse-accessForce-bids-api
# API Documentation

This API stores and serves information about Methods bids for client tenders.

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
4. Install Makefile if not already installed. You can check if it is installed by running the following command:

      ```bash
      make --version
      ```
5. Version 3.81 or higher is required. If you do not have Make installed, you can install it with Homebrew:

      ```bash
      brew install make
      ```
6. Run the following command to have all the commands to use the API with Makefile:

      ```bash
      make help
      ```
7. Run the following command to start the API:

      ```bash
      make run
      ```
 * The API will be available at http://localhost:8080/api/bids

8. Follow this link to go to the authorization documentation: [Authorization Documentation](https://github.com/methods/tdse-accessForce-auth-stub/blob/main/README.md)


9. In a new terminal enter the following command to run authorization server if not already running. This will be needed to generate a token:

      ```bash
      make auth
      ```
 * The API will be available at http://localhost:5000/authorise

--------------

## Environmental Variables

In order to validate your credentials and configure the database connection, you will have to set up the environmental variables locally.

To do this, create a `.env` file in your root folder, with the following key/value pairs:

      API_KEY=THIS_IS_THE_API_KEY
      SECRET_KEY=THIS_IS_A_SECRET
      DB_HOST=localhost
      DB_NAME=bidsAPI
      TEST_DB_NAME=testAPI

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
      make mongostart
      ```
4. To verify that MongoDB is running, run:

      ```bash
      brew services list
      ```
   You should see the service `mongodb-community` listed as `started`.
5. Run the following command to stop the MongoDB instance, as needed:

      ```bash
      make mongostop
      ```
6. To begin using MongoDB, connect the MongoDB shell (mongosh) to the running instance. From a new terminal, issue the following:

      ```bash
      mongosh
      ```
7. To create a new database called `bidsAPI`, run:

      ```bash
      use bidsAPI
      ```
8. To create a test database called `testAPI`, run:

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

## Accessing API Documentation (Swagger Specification)

1. Run the following command to start the API:

      ```bash
      make run
      ```
2. In a new terminal run the following command to open the Swagger UI in your default web browser:
      
      ```bash
      make swag
      ```
--------------

## Testing the application

1. Run the following command to start the API (if not already started):

      ```bash
      make run
      ```
2. Run the following command to start the Auth stub (if not already started):

      ```bash
      make auth
      ```
3. Run the following command to start the MongoDB instance (if not already started):

      ```bash
      make mongostart
      ```
4. Run the following command to setup the test database:

      ```bash
      make test-setup
      ```
5. In a new terminal enter the following command to run the test suites and generate a test coverage report:
      
      ```bash
      make test
      ```

--------------

## Using auth playground to generate a token and make authenticated requests to the Bids API

1. Follow the steps in the section above to start the API and authorization server.

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
