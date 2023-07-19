from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.controllers.bid_controller import bid

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger_config.yml'  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Bids API Swagger"
    })

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(bid, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=8080)