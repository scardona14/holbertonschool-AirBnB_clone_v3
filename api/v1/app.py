#!/usr/bin/python3

"""Module for API views"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify


app = Flask(__name__)

app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(exception):
    """ Handles 404 """
    return jsonify(error="Not found"), 404

@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(
        host='0.0.0.0' if host is None else host,
        port=5000 if port is None else port,
        threaded=True)
