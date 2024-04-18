#!/usr/bin/python3

"""Index module for the API"""

from api.v1.views import app_views, index
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return stats"""
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )


def count(cls):
    """Count the number of objects in storage"""
    return storage.count(cls)
