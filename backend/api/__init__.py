"""Initialize the backend."""
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # manages tokens to allow user access to routes/services
from flask_bcrypt import Bcrypt  # encrypts passwords


# create the flask object 
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)#, resources= {
#     r"/location": {"origins": "http://127.0.0.1"},
#     r"/": {"origins": "http://127.0.0.1"},
#     r"/location": {"origins": "http://127.0.0.1"},
#     r"/auth": {"origins": "http://127.0.0.1"},
#     r"/register": {"origins": "http://127.0.0.1"},
#     r"/api/location": {"origins": "http://127.0.0.1"}
# })
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

"""Cookie setup."""
"""See https://flask-jwt-extended.readthedocs.io/en/stable/tokens_in_cookies/."""
# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Maybe set this for production server!
# app.config['JWT_COOKIE_DOMAIN'] = '.dev.org'

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = os.environ.get('ENV') == 'production'

app.config['JWT_COOKIE_SAMESITE'] = 'strict'  # lax

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/location'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Use modified encoder class to handle ObjectId & datetime object while jsonifying the response.
class JSONEncoder(json.JSONEncoder):
    """Extend json-encoder class."""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return json.JSONEncoder.default(self, o)


app.json_encoder = JSONEncoder


from api.controllers import *

"""Create admin account if in testing branch"""
with app.app_context():
    if(os.environ.get('ENV') == 'development') and mongo.db.users.find_one({'email':'admin@vs.com'}) is None:
        data = {
            'email': 'admin@vs.com', 
            'password': flask_bcrypt.generate_password_hash(os.environ.get('DEV_ADMIN_PASSWORD')),
            'roles': ['admin','member']
        }
        mongo.db.users.insert_one(data)