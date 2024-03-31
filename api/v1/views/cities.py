#!/usr/bin/python3
"""This module handles the HTTP methods for cities"""

from flask import jsonify, abort, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_state(state_id):
    """Returns a list of all Cities in a State"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Returns information about a single city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city from the database"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city in the database"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json(silent=True):
        return jsonify(400, 'Not a JSON')
    data = request.get_json(silent=True)
    if 'name' not in data:
        return abort(400, 'Missing name')
    data['state_id'] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city in the database"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json(silent=True):
            return abort(400, 'Not a JSON')

        data = request.get_json(silent=True)
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
