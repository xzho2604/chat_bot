#Python 2.7.6
#RestfulClient.py

import httplib2
import requests
from requests.auth import HTTPDigestAuth
import json

URL = "http://api.openweathermap.org/data/2.5"


city_name = 'London'
api_key = 'dcab36878042169db010d12e64498409'

#helper function that interact with weather API and get back with the result
def get_weather(city_name):

    url = URL + '/weather?q=' + city_name + '&' +  'APPID=' + api_key
    print(url)
    http = httplib2.Http()
    content_type_header = "application/json"

    headers = {'Content-Type': content_type_header}
    response, content = http.request(url,
                                     'GET',
                                     headers=headers)
    print('status:', response['status'])
    content = json.loads(content)
    weather = content['weather'][0]['main']
    print('The weather now in ' + city_name + ' is ' + weather)
    return weather

#return the client requery result
def weather_service(req):
    city = req["queryResult"]["parameters"]["address"]["city"]
    #get the location parametre from the res and send to the weather API
    weather = get_weather(city)
    print("the weather we get back is " + weather)

    speech = "The weather in " + city + ": " + weather
    result = {
    "fulfillmentText": speech,
     "source": "Open Weather"
    }

    return result



if __name__=="__main__":
    print("main")
    get_weather(city_name)
