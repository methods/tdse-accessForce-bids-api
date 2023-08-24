"""
This is a simple Python application.

"""
import json
import logging
import logging.config
import traceback
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from api.controllers.bid_controller import bid
from api.controllers.question_controller import question


# Load the configuration from the JSON file
with open("logconfig/logging_config.json", "r") as f:
    config = json.load(f)

# Configure the logger using dictConfig
logging.config.dictConfig(config)
logger = logging.getLogger()

app = Flask(__name__)


# Custom middleware to log requests
@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url} {request.endpoint}")


SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/static/swagger_config.yml"  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Bids API Swagger"},
)

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(bid, url_prefix="/api")
app.register_blueprint(question, url_prefix="/api")


if __name__ == "__main__":
    logger.debug("Starting application")
    app.run(port=8080)
