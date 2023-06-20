from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/helloworld')
def hello_world():
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True, port=4000)