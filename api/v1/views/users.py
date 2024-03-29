from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'])
def get_user():
    users = storage.get(User)
    return jsonify([user.to_dict() for user in users.values])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    return jsonify(u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):


@app_views.route('/users', methods=['POST'])
def create_user():


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):