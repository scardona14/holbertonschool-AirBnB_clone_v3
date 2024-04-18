#!/usr/bin/python3

"""Index module for the API"""

from api.v1.views import app_views
from flask import jsonify



@app_views.route('/status', methods=['GET'])
def status():
    """Return status"""
    return jsonify({"status": "OK"})

