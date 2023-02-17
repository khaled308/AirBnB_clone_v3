#!/usr/bin/python3
""" Place_reviews API """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def place_review_func(place_id):
    """ Handles place-specific review methodes """
    places = storage.all(Place)
    reviews = storage.all(Review)
    key = "Place." + place_id

    # GET method
    if request.method == "GET":
        try:
            place = places[key]
            revlist = [rev.to_dict() for rev in place.reviews]
            return jsonify(revlist)
        except KeyError:
            abord(404)

    # POST method
    if request.method == "POST":
        if not request.is_json:
            abort(400, "Not a JSON")

        body = request.get_json()

        if "user_id" not in body:
            abort(400, "Missing user_id")
        elif "text" not in body:
            abort(400, "Missing text")
        else:
            users = storage.all(User)
            uid = body['user_id']
            all_uid = [uids.id for uids in users.values()]
            if uid not in all_uid:
                abort(404)
            if key not in places:
                abort(404)

            body.update({"place_id": place_id})
            new = Review(**body)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

    # If you get here, request isn't supported in the code
    abort(501)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def review_id_func(review_id):
    """ Handles specific review id methods """
    reviews = storage.all(Review)
    key = "Review." + review_id

    # GET method
    if request.method == "GET":
        if review_id:
            try:
                return jsonify(reviews[key].to_dict())
            except KeyError:
                abort(404)
        else:
            return jsonify(obj.to_dict() for obj in reviews.values())

    # DELETE method
    if request.method == "DELETE":
        try:
            storage.delete(reviews[key])
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

    # PUT method
    if request.method == "PUT":
        try:
            review = reviews[key]
        except KeyError:
            abort(404)

        if not request.is_json:
            abort(400, "Not a JSON")

        new = request.get_json()
        for rkey, value in new.items():
            if rkey not in ["id", "user_id", "place_id",
                            "created_at", "updated_at"]:
                setattr(review, rkey, value)
            storage.save()
        return review.to_dict(), 200

    # If you get here, request isn't supported in the code
    abort(501)
