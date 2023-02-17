#!/usr/bin/python3
"""Index.py file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    """Routes to status page"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    """Retrieves the number of each object by type"""
    count_dict = {}
    for _class in classes:
        count_dict[_class] = storage.count(classes[_class])
    return jsonify(count_dict)
