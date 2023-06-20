from flask import Blueprint

from controllers.hello_controller import hello_world

hello = Blueprint('hello', __name__)

@hello.route('/helloworld')
def hey_world():
    return hello_world()