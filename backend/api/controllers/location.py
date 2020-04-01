"""Controller and routes for ."""
from flask import request, jsonify
from api import app, mongo
import os
import logger


ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

LOG.info("Loaded api.controllers.location.py")


@app.route('/location_public', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def location_public():
    if request.method == 'GET':
        requestArgs = request.args

        try:
            if requestArgs.get('queryType') is None:
                return jsonify('queryType not specified you motherfucker! Specify either queryType=loc or label to perform a query')
        except AttributeError as err:
            return jsonify('No arguments passed: Please pass queryType and latMin/Max, longMin/Max')

        if requestArgs.get('queryType') == "loc":

            # get locations from db
            if requestArgs.get('latMax') is not None and \
               requestArgs.get('latMin') is not None and \
               requestArgs.get('longMax') is not None and \
               requestArgs.get('longMin') is not None:
                data = list(mongo.db.loc_public.find(
                    {'latitude': {'$lte': float(requestArgs.get('latMax')),
                                  '$gte': float(requestArgs.get('latMin'))},
                     'longitude': {'$lte': float(requestArgs.get('longMax')),
                                   '$gte': float(requestArgs.get('longMin'))}}))
            elif requestArgs.get('latMax') is not None and \
              requestArgs.get('latMin') is not None and \
              requestArgs.get('longMax') is None and \
              requestArgs.get('longMin') is None:
                data = list(mongo.db.loc_public.find(
                    {'latitude': {'$lte': float(requestArgs.get('latMax')),
                                  '$gte': float(requestArgs.get('latMin'))}}))
            elif requestArgs.get('latMax') is None and \
              requestArgs.get('latMin') is None and \
              requestArgs.get('longMax') is not None and \
              requestArgs.get('longMin') is not None:
                data = list(mongo.db.loc_public.find(
                    {'longitude': {'$lte': float(requestArgs.get('longMax')),
                                   '$gte': float(requestArgs.get('longMin'))}}))
            return jsonify(data), 200

        elif requestArgs.get('queryType') == "label":
            label = requestArgs['label']
            if label is not None:
                data = list(mongo.db.loc_public.find({'label': label}))
            return jsonify(data), 200

        else:
            return jsonify("Invalid queryType specified, asshole! Specify either 'loc' \
                            or 'label' to perform a query"), 400

    data = request.get_json()
    if request.method == 'POST':
        if data.get('latitude', None) is not None and data.get('longitude', None) is not None:
            mongo.db.loc_public.insert_one(data)
            return jsonify({'ok': True, 'message': 'Location created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('latitude', None) is not None:
            db_response = mongo.db.loc_public.delete_one({'latitude': data['latitude']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
        if data.get('longitude', None) is not None:
            db_response = mongo.db.loc_public.delete_one({'longitude': data['longitude']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.loc_public.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

#staged location api endpoints
@app.route('/location_staged', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def location_staged():
    if request.method == 'GET':
        requestArgs = request.args
        # get staged locations from db
        data = list(mongo.db.loc_staged.find())      
        return jsonify(data), 200


    data = request.get_json()
    if request.method == 'POST':
        if data.get('latitude', None) is not None and \
          data.get('longitude', None) is not None and \
          data.get('label', None) is not None and \
          data.get('user_id', None) is not None:
            # minimal data for inserting a location
            if data.get('category', None) is not None:
                mongo.db.loc_staged.insert_one({'label': data['label'],
                                     'latitude': data['latitude'],
                                     'longitude': data['longitude'],
                                     'user_id': data['user_id'],
                                     'category': data['category']})
            else:
                mongo.db.loc_staged.insert_one({'label': data['label'],
                                     'latitude': data['latitude'],
                                     'longitude': data['longitude'],
                                     'user_id': data['user_id']}) 
            return jsonify({'ok': True, 'message': 'Location created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('latitude', None) is not None and \
          data.get('longitude', None) is not None and \
          data.get('label', None) is not None and \
          data.get('user_id', None) is not None:
            db_response = mongo.db.loc_staged.delete_one({'label': data['label'],
                                     'latitude': data['latitude'],
                                     'longitude': data['longitude'],
                                     'user_id': data['user_id'],
                                     'category': data['category']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        # new doc must contain the new json document containing the updated properties
        if data.get('new_doc', None) is not None and \
          data.get('latitude', None) is not None and \
          data.get('longitude', None) is not None and \
          data.get('label', None) is not None and \
          data.get('user_id', None) is not None:
            mongo.db.loc_staged.replace_one(
                {'label': data['label'],'latitude': data['latitude'],'longitude': data['longitude'],'user_id': data['user_id']},
                data.get('new_doc', {}) )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400