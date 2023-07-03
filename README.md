# tdse-accessForce-bids-api
# API Documentation

This API provides an endpoint to post a new bid document.

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
8. The API will be available at http://localhost:8080/api/bids

--------------

## Accessing API Documentation (Swagger Specification)

1. Run the following command to start the API:

      ```bash
      python app/app.py
      ```
2. The Swagger Specification will be available at http://localhost:8080/api/docs


### Contributing to this project

See [CONTRIBUTING](https://github.com/methods/tdse-accessForce-bids-api/blob/main/CONTRIBUTING.md) for details

### License

See [LICENSE](https://github.com/methods/tdse-accessForce-bids-api/blob/main/LICENSE.md) for details
