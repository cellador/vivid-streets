"""Controller and routes for ."""
from flask import request, jsonify
from api import app, mongo
import os
import logger
import json

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

LOG.info("Loaded api.controllers.location.py")

@app.route('/location', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def location():
    if request.method == 'GET':
        query = request.args
        queryJson = request.get_json()

        if queryJson.get('queryType', None) is None:
            return jsonify("queryType not specified you motherfucker! Specify either 'loc' or 'label' to perform a query")
        
        if queryJson['queryType'] == "loc":

            # get locations from db
            if queryJson.get('latMax', None) is not None and queryJson.get('latMin', None) is not None and queryJson.get('longMax', None) is not None and queryJson.get('longMin', None) is not None:
                data = list(mongo.db.loc.find({'latitude': {'$lte': queryJson.get('latMax', None), '$gte': queryJson.get('latMin', None)}, 'longitude': {'$lte': queryJson.get('longMax', None), '$gte': queryJson.get('longMin', None)}}))
            elif queryJson.get('latMax', None) is not None and queryJson.get('latMin', None) is not None and queryJson.get('longMax', None) is None and queryJson.get('longMin', None) is None:
                data = list(mongo.db.loc.find({'latitude': {'$lte': queryJson.get('latMax', None), '$gte': queryJson.get('latMin', None)}}))
            elif queryJson.get('latMax', None) is None and queryJson.get('latMin', None) is None and queryJson.get('longMax', None) is not None and queryJson.get('longMin', None) is not None:
                data = list(mongo.db.loc.find({'longitude': {'$lte': queryJson.get('longMax', None), '$gte': queryJson.get('longMin', None)}}))
            return jsonify(data), 200

        elif queryJson['queryType'] == "label":
            label = queryJson['label']
            if label is not None:
                data = list(mongo.db.loc.find({'label': label}))
            return jsonify(data), 200

        else:
            return jsonify("Invalid queryType specified, asshole! Specify either 'loc' or 'label' to perform a query"), 400

    data = request.get_json()
    if request.method == 'POST':
        if data.get('latitude', None) is not None and data.get('longitude', None) is not None and data.get('label', None) is not None:
            # minimal data for inserting a location
            mongo.db.loc.insert_one({'label': data['label'], 'latitude': data['latitude'], 'longitude': data['longitude']})
            return jsonify({'ok': True, 'message': 'Location created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('latitude', None) is not None:
            db_response = mongo.db.loc.delete_one({'latitude': data['latitude']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
        if data.get('longitude', None) is not None:
            db_response = mongo.db.loc.delete_one({'longitude': data['longitude']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.loc.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
