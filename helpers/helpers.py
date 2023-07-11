from flask import jsonify
import uuid
from datetime import datetime

def showConnectionError():
    return jsonify({"Error": "Could not connect to database"}), 500

def showNotFoundError():
    return jsonify({"Error": "Not found"}), 404

def is_valid_uuid(string):
    try:
        uuid.UUID(str(string))
        return True
    except ValueError:
        return False
    
def is_valid_isoformat(string):
    try:
        datetime.fromisoformat(string)
        return True
    except:
        return False