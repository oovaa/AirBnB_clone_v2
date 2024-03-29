#!/usr/bin/python3
"""Starts a Flask web application."""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
