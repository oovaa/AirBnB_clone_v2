#!/usr/bin/python3
""" File containing review module"""
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    """Get reviews by place_id"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    reviews = [obj.to_dict() for obj in p.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get review by review_id"""
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review by review_id"""
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    r.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create review by place_id"""
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': "Missing user_id"}), 400
    if 'text' not in request.get_json():
        return jsonify({'error': "Missing text"}), 400
    data = request.get_json()
    data['place_id'] = place_id
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    obj = Review(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update review by review_id"""
    if not request.get_json():
        return jsonify({'error': "Not a JSON"}), 400
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(r, k, v)
    storage.save()
    return jsonify(r.to_dict()), 200
