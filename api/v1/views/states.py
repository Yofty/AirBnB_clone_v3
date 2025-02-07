#!/usr/bin/python3
"""
this script containes lists all the states.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """ get all by id """
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """ get state by id"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ delete state by id"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """ create new instance """
    new_obj = request.get_json()
    if not new_obj:
        abort(400, "Not a JSON")
    if 'name' not in new_obj:
        abort(400, "Missing name")
    obj = State(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ post method """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)


    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")


    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
