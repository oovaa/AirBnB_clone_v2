from flask import jsonify, abort, request
from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([place.to_dict() for place in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):