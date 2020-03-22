''' flask app with mongo '''
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
#Part 3 of tutorial
from flask_jwt_extended import JWTManager #JWT used for securely transmitting information as JSON, creates tokens?
from flask_bcrypt import Bcrypt #encrypts passwords to be saved in db

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    # def default(self, o):
    #     if isinstance(o, ObjectId):
    #         return str(o)
    #     if isinstance(o, datetime.datetime):
    #         return str(o)
    #     return json.JSONEncoder.default(self, o)

    # Part 3 of tutorial
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)



# create the flask object
app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

# Part 3 of tutorial
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
# Part 3: encrypts password
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder

from api.controllers import *
