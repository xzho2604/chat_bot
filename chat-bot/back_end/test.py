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
def webhook():
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason

    print("Request:")
    #print(json.dumps(req, indent=4)) #print out the hierachy of python dict in json format

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='127.0.0.1')
