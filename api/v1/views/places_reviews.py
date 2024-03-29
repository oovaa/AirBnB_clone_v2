from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    p = storage.get(Review, place_id)
    if p is None:
        abort(404)
    return jsonify([place.to_dict() for place in p.cities])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    pass


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    pass


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    pass
