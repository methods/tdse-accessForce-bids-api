"""
This is a simple Python application.

"""

from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from api.controllers.bid_controller import bid
from api.controllers.question_controller import question
from datetime import datetime, timedelta


app = Flask(__name__)

SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/static/swagger_config.yml"  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Bids API Swagger"},
)

request_history = {}  # Store request history for throttling


@app.before_request
def backend_throttling_middleware():
    user_ip = request.remote_addr
    current_time = datetime.now()

    # Define the maximum requests per second (configurable)
    max_requests_per_second = 2

    # Check if user IP exists in the request history
    if user_ip in request_history:
        # Calculate the time elapsed since the last request
        time_elapsed = current_time - request_history[user_ip]
        if time_elapsed < timedelta(seconds=1 / max_requests_per_second):
            # Throttle the request and return an error response with Retry-After header
            retry_after = (1 / max_requests_per_second) - time_elapsed.total_seconds()
            response = jsonify({"error": "Too many requests. Please try again later."})
            return response, 429, {"Retry-After": int(retry_after)}

    # Update the request history with the current time
    request_history[user_ip] = current_time


app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(bid, url_prefix="/api")
app.register_blueprint(question, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
