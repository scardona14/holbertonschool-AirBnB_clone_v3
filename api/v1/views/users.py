#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
from flasgger.utils import swag_from                                                  

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/users_get.yml')
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/users_id_get.yml')
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'],
                  strict_slashes=False)
@swag_from('swagger_yaml/users_id_delete.yml', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/users_post.yml', methods=['POST'])
def post_user():
    """Creates a User"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/users_id_put.yml', methods=['PUT'])
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
