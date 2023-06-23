from flask import Flask
from flasgger import Swagger

from api.controllers.bid_controller import bid

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(bid, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=3000)