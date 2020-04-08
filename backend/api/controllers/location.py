"""Controller and routes for ."""
import os
import logger
from flask import request, jsonify
from api import app, mongo
from api.schemas import validate_location
from api.decorators import roles_required
from flask_jwt_extended import (jwt_required, get_jwt_identity)

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

LOG.info("Loaded api.controllers.location.py")


@app.route('/location', methods=['GET'])
def getPublicLocation():
    """Handle public locations."""
    if request.method == 'GET':
        return _GET(request.args, mongo.db.loc_public)


@app.route('/location/staged', methods=['GET'])
@jwt_required
@roles_required('admin')
def getStagedLocation():
    """Handle private locations."""
    if request.method == 'GET':
        return _GET(request.args, mongo.db.loc_staged)


def _GET(requestArgs, collection):
    # Enforce queryType
    try:
        queryType = requestArgs.get('queryType', type=str)

        if queryType != "loc" and queryType != "label":
            raise AttributeError()

    except AttributeError as err:
        return jsonify(
            'Invalid URI parameter "queryType". Values allowed: "loc" and "label"'), 400

    if queryType == "loc":
        # get locations from db
        if requestArgs.get('latMax') is not None and \
          requestArgs.get('latMin') is not None and \
          requestArgs.get('longMax') is not None and \
          requestArgs.get('longMin') is not None:
            data = list(collection.find(
                {'latitude': {'$lte': float(requestArgs.get('latMax')),
                              '$gte': float(requestArgs.get('latMin'))},
                 'longitude': {'$lte': float(requestArgs.get('longMax')),
                               '$gte': float(requestArgs.get('longMin'))}}))
        elif requestArgs.get('latMax') is not None and \
          requestArgs.get('latMin') is not None and \
          requestArgs.get('longMax') is None and \
          requestArgs.get('longMin') is None:
            data = list(collection.find(
                {'latitude': {'$lte': float(requestArgs.get('latMax')),
                              '$gte': float(requestArgs.get('latMin'))}}))
        elif requestArgs.get('latMax') is None and \
          requestArgs.get('latMin') is None and \
          requestArgs.get('longMax') is not None and \
          requestArgs.get('longMin') is not None:
            data = list(collection.find(
                {'longitude': {'$lte': float(requestArgs.get('longMax')),
                               '$gte': float(requestArgs.get('longMin'))}}))
        else:
            data = list(collection.find())
        return jsonify(data), 200

    elif queryType == "label":
        label = requestArgs['label']
        if label is not None:
            data = list(collection.find({'label': label}))
        else:
            data = list(collection.find())
        return jsonify(data), 200


@app.route('/location/staged', methods=['POST', 'DELETE', 'PATCH'])
@jwt_required
@roles_required('member')
def postStagedLocation():
    """Post staged location.

    Only accessible for member and admin.
    """
    # Enforce collection
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify('Request body must be JSON.'), 400

    user = get_jwt_identity()
    data['user_id'] = user['_id']

    if request.method == 'POST':
        return _POST(data, mongo.db.loc_staged)

    if request.method == 'DELETE':
        return _DELETE(data, mongo.db.loc_staged)

    if request.method == 'PATCH':
        return _PATCH(data, mongo.db.loc_staged)


def _POST(data, collection):
    data = validate_location(data)  # Check if received data valid and in required format
    if data['ok']:
        collection.insert_one(data)
        return jsonify({'ok': True, 'message': 'Location created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'
                        .format(data['message'])}), 400


def _DELETE(data, collection):
    pass  # Delete stub, could be implemented as above using a schema or as below


def _PATCH(data, collection):
    pass  # Patch stub, could be implemented as above using a schema or as below

# #staged location api endpoints
# @app.route('/location_staged', methods=['GET', 'POST', 'DELETE', 'PATCH'])
# def location_staged():
#     if request.method == 'GET':
#         requestArgs = request.args
#         # get staged locations from db
#         data = list(mongo.db.loc_staged.find())
#         return jsonify(data), 200
#     data = request.get_json()
#     if request.method == 'POST':
#         if data.get('latitude', None) is not None and \
#           data.get('longitude', None) is not None and \
#           data.get('label', None) is not None and \
#           data.get('user_id', None) is not None:
#             # minimal data for inserting a location
#             if data.get('category', None) is not None:
#                 mongo.db.loc_staged.insert_one({'label': data['label'],
#                                      'latitude': data['latitude'],
#                                      'longitude': data['longitude'],
#                                      'user_id': data['user_id'],
#                                      'category': data['category']})
#             else:
#                 mongo.db.loc_staged.insert_one({'label': data['label'],
#                                      'latitude': data['latitude'],
#                                      'longitude': data['longitude'],
#                                      'user_id': data['user_id']})
#             return jsonify({'ok': True, 'message': 'Location created successfully!'}), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

#     if request.method == 'DELETE':
#         if data.get('latitude', None) is not None and \
#           data.get('longitude', None) is not None and \
#           data.get('label', None) is not None and \
#           data.get('user_id', None) is not None:
#             db_response = mongo.db.loc_staged.delete_one({'label': data['label'],
#                                      'latitude': data['latitude'],
#                                      'longitude': data['longitude'],
#                                      'user_id': data['user_id'],
#                                      'category': data['category']})
#             if db_response.deleted_count == 1:
#                 response = {'ok': True, 'message': 'record deleted'}
#             else:
#                 response = {'ok': True, 'message': 'no record found'}
#             return jsonify(response), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

#     if request.method == 'PATCH':
#         # new doc must contain the new json document containing the updated properties
#         if data.get('new_doc', None) is not None and \
#           data.get('latitude', None) is not None and \
#           data.get('longitude', None) is not None and \
#           data.get('label', None) is not None and \
#           data.get('user_id', None) is not None:
#             mongo.db.loc_staged.replace_one(
#                 {'label': data['label'],'latitude': data['latitude'],'longitude': data['longitude'],'user_id': data['user_id']},
#                 data.get('new_doc', {}) )
#             return jsonify({'ok': True, 'message': 'record updated'}), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
