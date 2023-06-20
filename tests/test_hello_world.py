from flask import Flask
import pytest

from controllers.hello_controller import hello_world

from routes.hello_route import hello

def test_hello_world():
    result = hello_world()
    assert result == 'Hello, World!'

@pytest.fixture   
def client():
    app = Flask(__name__)
    app.register_blueprint(hello, url_prefix='/api')
    with app.test_client() as client:
        yield client

def test_hello_world_route(client):
    response = client.get('/api/helloworld')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, World!'