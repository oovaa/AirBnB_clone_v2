#!/usr/bin/python3
"""This module handles the HTTP methods for cities"""

from flask import jsonify, abort, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_city_state(state_id):
    """Returns a list of all Cities in a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([place.to_dict() for place in state.cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """Returns information about a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city from the database"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new city in the database"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    js = request.get_json()
    obj = City(**js)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city in the database"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
