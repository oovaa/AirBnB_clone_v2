#!/usr/bin/python3
"""Places view module"""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Get all places in a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Get a specific place by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new place in a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    if 'user_id' not in data_dict:
        abort(400, description="Missing user_id")
    user = storage.get(User, data_dict['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data_dict:
        abort(400, description="Missing name")
    data_dict['city_id'] = city_id
    new_place = Place(**data_dict)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a place by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    for k, v in data_dict.items():
        if k not in ("id", "user_id", "city_id", "created_at", "updated_at"):
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
