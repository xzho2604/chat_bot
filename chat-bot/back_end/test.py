# Updated in July 2018 to reflect Dialogflow v2 changes for request/response
# Author - Naresh Ganatra
# http://youtube.com/c/NareshGanatra
from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response

#import third party services apis functions
from  api_service.weather_api import *

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/', methods=['POST'])
#@app.route('/', methods=['GET'])
def test():
    print("I am here ==================")
    print(request)
    return "hello out"

if __name__ == '__main__':
    app.run()
