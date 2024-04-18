#!/usr/bin/python3

"""Index module for the API"""

from api.v1.views import app_views, index
from flask import jsonify
from models import storage



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
