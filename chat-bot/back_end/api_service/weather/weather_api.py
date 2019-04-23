
import httplib2
import requests
from requests.auth import HTTPDigestAuth
import json
import xmltodict
import datetime

URL = "http://api.openweathermap.org/data/2.5"


city_name = 'London'
api_key = 'dcab36878042169db010d12e64498409'

#given the request extract the city name and gives forcast wthin 5 days
def get_forecast(city_name,when):
    #city_name = req['queryResult']['parameters']['address']['city']

    ret_dict = {} #store the result of the enqury
    date_arr= ["mon","tue",'wed',"thu","fri","sat","sun"]
    weather = ""

    url = URL + '/forecast?q=' + city_name + '&' + 'APPID=' + api_key + '&' + 'mode=xml'
    #print(url)
    http = httplib2.Http()
    content_type_header = "application/xml"

    headers = {'Content-Type': content_type_header}
    response, content = http.request(url,'GET',headers=headers)
    xmlparse = xmltodict.parse(content)

    #time from 2019-04-03T06:00:00 2019-04-03T09:00:00 time to few clouds
    for i in range (len(xmlparse['weatherdata']['forecast']['time'])):
        time = xmlparse['weatherdata']['forecast']['time'][i]['@from'] #get the from time of forcast
        year = time[:4]
        month = time[5:7]
        day= time[8:10]
        date = datetime.date(int(year),int(month),int(day))
        print("The date is :",date,when)

        if(time[11:] == '12:00:00' and str(date)  == when): #only get the noon time weather as that day weather
            weather =xmlparse['weatherdata']['forecast']['time'][i]['symbol']['@name']
            #ret_dict[date_arr[date.weekday()]]= weather
            #print(date_arr[date.weekday()],weather)
    
    print(weather)
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
    get_forecast("sydney","2019-04-24T12:00:00+10:00")


'''
#give city name return single day weather forcaset
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

'''
