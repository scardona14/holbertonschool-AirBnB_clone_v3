#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/places_reviews_get.yml', methods=['GET'])
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('swagger_yaml/reviews_id_get.yml', methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('swagger_yaml/reviews_id_delete.yml', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                    strict_slashes=False)
@swag_from('swagger_yaml/places_reviews_post.yml', methods=['POST'])
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_json:
        abort(400, 'Missing user_id')
    user = storage.get(User, review_json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in review_json:
        abort(400, 'Missing text')
    review_json['place_id'] = place_id
    review = Review(**review_json)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                    strict_slashes=False)
@swag_from('swagger_yaml/reviews_id_put.yml', methods=['PUT'])
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_json.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
