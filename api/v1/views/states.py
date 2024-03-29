#!/usr/bin/python3
"""This module handles the HTTP methods for states"""

from flask import request
from flask import json, jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """Returns a list of all states in the database"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Get information about a specific state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state from the database given its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new state with data sent in the request"""
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    if 'name' not in data_dict:
        abort(400, description="Missing name")
    new_state = State(**data_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a state with data sent in the request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    for k, v in data_dict.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
