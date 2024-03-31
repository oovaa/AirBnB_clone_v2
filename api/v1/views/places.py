#!/usr/bin/python3
"""Places view module"""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Get all places in a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a specific place by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place by its id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
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


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.update(state.places)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places
                  if amenities_set.issubset(set(amen.id))
                  for amen in place.amenities]
    return jsonify([place.to_dict() for place in places])
