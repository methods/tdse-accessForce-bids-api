from flask import Flask

from api.routes.bid_route import bid

app = Flask(__name__)

app.register_blueprint(bid, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=3000)