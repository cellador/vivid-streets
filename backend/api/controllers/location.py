"""Controller and routes for ."""
from flask import request, jsonify
from api import app, mongo
import os
import logger


ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

LOG.info("Loaded api.controllers.location.py")


@app.route('/location', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def location():
    if request.method == 'GET':
        query = request.args
        data = list(mongo.db.loc.find(query)) 
        return jsonify(data), 200

    data = request.get_json()
    if request.method == 'POST':
        if data.get('latitude', None) is not None and data.get('longitude', None) is not None:
            mongo.db.loc.insert_one(data)
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
