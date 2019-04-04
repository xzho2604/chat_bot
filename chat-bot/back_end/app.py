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
from  api_service.weather.weather_api import *
from  api_service.music.spotify_api import *
from helper import *

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason

    print("Request:")
    #print(json.dumps(req, indent=4)) #print out the hierachy of python dict in json format

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#process the request and return the response accordingly
def processRequest(req):
    action = req["queryResult"]["action"] 
    param = req['queryResult']['parameters']

    print("the action now is :",action) 
    
    #fullfill weather
    if action == "weather": #perform weather service
        result = {
            "fulfillmentText": "~",
            "source":json.dumps(process_weather(param)), 
            #"ans":process_weather(param)
        }


    elif action == "music.play":
        print("now in music")
        result = show_recommendations_for_artist(req)
        print("the returned content:",result["contents"],type(result["contents"]))
        music_name = result["contents"][0]["name"]
        url = result["contents"][0]["url"]
        result = {
            "fulfillmentText": url,
            "source": "spotify"
        }


    else:
        print ("Please check your action name in DialogFlow...")
        return {}
    
    #other actions 

    return result 

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')

'''
def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)
    #Naresh
    return {

    "fulfillmentText": speech,
     "source": "Yahoo Weather"
    }


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message ="this is the message"

    my_result =  {

    "fulfillmentText": string,
     "source": string
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
'''
