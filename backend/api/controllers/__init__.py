''' flask app with mongo 
import os
import json
import datetime
from flask import Flask

# create the flask object
app = Flask(__name__) '''
''' all controllers for various collections of database '''
import os
import glob

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
