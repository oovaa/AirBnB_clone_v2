#!/usr/bin/python3
"""This module handles the HTTP methods for amenities"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Return all amenities in the system"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get a specific amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specific amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Create a new amenity with data from the request"""
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    if 'name' not in data_dict:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity with data from the request"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")
    for k, v in data_dict.items():
        if k not in ("id", "created_at", "updated_at"):
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
