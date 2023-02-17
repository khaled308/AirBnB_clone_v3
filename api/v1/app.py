#!/usr/bin/python3
"""app.py file"""
from models import storage
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(error):
    """
    Method that calls storage.close
    """
    storage.close()


@app.errorhandler(404)
def error_404(message):
    """
    404 error message
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    Setting host and port
    """
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = int(getenv("HBNB_API_PORT", default=5000))
    app.run(host=host, port=port, threaded=True)
