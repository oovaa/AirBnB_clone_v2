#!/usr/bin/python3
"""Module for endpoint (route) status"""

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review


@app_views.route('/status', methods=['GET'])
def status():
    """Endpoint that retrieves the status"""

    result = {
        "status": "OK"
    }
    return jsonify(result)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    result = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(result)
