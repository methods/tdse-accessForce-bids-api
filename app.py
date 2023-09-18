"""
This is a simple Python application.

"""

import json
import logging
import logging.config
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, g, request
from flask_swagger_ui import get_swaggerui_blueprint
from api.controllers.bid_controller import bid
from api.controllers.question_controller import question
from dbconfig.mongo_setup import get_db


load_dotenv()


# Load the configuration from the JSON file
with open("logconfig/logging_config.json", "r") as f:
    config = json.load(f)

# Configure the logger using dictConfig
logging.config.dictConfig(config)
logger = logging.getLogger()


# Swagger config
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/static/swagger_config.yml"  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Bids API Swagger"},
)


# App factory function
def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    # Register blueprints
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(bid, url_prefix="/api")
    app.register_blueprint(question, url_prefix="/api")

    # Create db client instance in application context
    with app.app_context():
        db = get_db(app.config["DB_HOST"], app.config["DB_PORT"], app.config["DB_NAME"])
        app.db = db

    # Custom middleware to log request info
    def log_request_info():
        request_id = uuid.uuid4()
        g.request_id = request_id
        logger.info(
            f"New request {g.request_id}: {request.method} {request.url} - - {request.endpoint}"
        )

    app.before_request(log_request_info)

    return app


if __name__ == "__main__":
    logger.debug("Starting application")
    app = create_app()
    app.run(port=8080)
