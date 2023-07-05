from flask import jsonify

def showConnectionError():
    return jsonify({"Error": "Could not connect to database"}), 500

def showNotFoundError():
    return jsonify({"Error": "Not found"}), 404