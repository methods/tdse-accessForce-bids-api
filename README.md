# tdse-accessForce-bids-api
# API Documentation

This API provides a simple "Hello World" message.

## Prerequisites

- Python 3.x
- Flask

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
8. The API will be available at http://localhost:3000


### Iterations

**Iteration 1** Build API and initial storage system to find, add, update and remove. Steps 1 to 8 from Must section

**Iteration 2** Secure the API to users who need access, based on the "Principle least priviledge principle. Step 9 from Must section

**Iteration 3** Build search engine to allow for a more sophisticated way of finding questions and bids related to your needs. Steps 1 and 2 from Should section

**Iteration 4** Expand on access control to bid library based on roles, users and teams where necessary. Step 1 of Could section

**Iteration 5** Host the bid library to be accessed by users across the country. Step 2 of Could section

**Iteration 6** Build a web app to integrate with the bids API, create user journeys that allow users to find, add and update bid content

--------------

**Note:** If this is part of your training, you should look for guidance by your mentor of how to progress this project. Your coach can use the [generic project rest API doc](/training/generic-projects/rest-api/README.md) to setup your initial project that will cover iteration 1.

--------------

Return to the [internal projects](https://github.com/methods/tdse-projects/blob/main/internal/README.md) for additional options and information.

--------------

### Contributing to this project

See [CONTRIBUTING](https://github.com/methods/tdse-accessForce-bids-api/blob/main/CONTRIBUTING.md) for details

### License

See [LICENSE](https://github.com/methods/tdse-accessForce-bids-api/blob/main/LICENSE.md) for details
