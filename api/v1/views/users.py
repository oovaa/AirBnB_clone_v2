#!/usr/bin/python3
"""Users view module"""

from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'])
def get_users():
    """Return all users in the system."""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Return a user in the system."""
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    return jsonify(u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user given its id."""
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    u.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create a new user with data from the request."""
    if not request.json:
        return


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user given its id and data from the request."""
    pass
