'''
Set up the key for authentication
Google Cloud:
1.IAM & Admin -> Roles-> add dialogflow roles and permissions
2.service account -> create service account -> add role and permission
2. API Services -> Crendentials -> create crednetials -> service account ->jason key
3. add os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'yourfilename.json' to tbe file to run
'''
#ssh -R chatbot:80:localhost:5000 serveo.net 
#static confiuration of the localhost to external internet

from __future__ import print_function
import os
import dialogflow
import sys
import socket
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask_assistant import context_manager
#music webhook fullfill is disabled process from the backedn
from api_service.music.spotify_api import *
from  api_service.weather.weather_api import *
from api_service.light.light_control import *
import random
from helper import *
import re



'''context api
context_client.delete_all_contexts(parent) #delete alll context
response = context_client.create_context(parent, context) #create context
context_client.delete_context(name) #delete a particular context
context_client.list_contexts(parent) #list all the context
'''


#============================================================================
#dialogflow client api config
#get access to the service key each service account has its key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account_key/weather_key.json'

#function to pass input and get back the response
def detect_intent_texts(project_id, session_id, texts, language_code):
    #set up session client
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #set up context client to manipulate context
    context_client = dialogflow.ContextsClient()
    parent = context_client.session_path(project_id, session_id)


    for text in texts:
        #extract parametres from the response
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        intent = response.query_result.intent.display_name
        action  = response.query_result.action
        param = response.query_result.parameters
        fulfillment = response.query_result.fulfillment_text


        print("the intent name is:",intent)
        print("the action is",action)
        for p in param:
            print("the para is" ,p,"with:", param[p])
        print('Fulfillment text: {}\n'.format(fulfillment))
       
        return context_client, parent,param, action ,fulfillment
        #print(response)

#get the project id from google cloud of the dialogflow agent
project_id = 'weather-f22a9'  
session_id = 'first'  #API caller defined
#============================================================================
'''
app = Flask(__name__)
#return to the fron end json:id,text,type
@app.route('/', methods=['POST'])
#@app.route('/', methods=['GET'])
def backend():
    #extrac the relevant parametrs from the front end 
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason
    params = req['params']
    object_id= params['ObjectID']
    query = params['query']
    print("query:",query)
    
    context_client, parent,param,action,fullfill_text = detect_intent_texts(project_id,session_id,[query],"en-US")
    #print("action:",action)
    #print("fullfilltext:",fullfill_text)

    tp = 'text' #type init as text
    if(fullfill_text): #if there is response means not the end asking for params so pass as text
        print(fullfill_text,type(fullfill_text),"type:",tp)
        res=  {'ObjectID': object_id, 'res': fullfill_text,'type':"text"}
        res = json.dumps(res)
        return jsonify(res)
    
    #here means the final process , to fullfill in the backend
    if(action == "music.getSongsByArtist"): #get artist return a recomended song
        fullfill_text=artist_song(param)
        tp ="music"
    if(action == "music.getAlbumListByArtist"): #get artist return an album
        fullfill_text=artist_album(param)
        tp ="music"
    if(action == "music.playSong"): #get song play a single song
        fullfill_text=play_song(param)
        tp = "music"
    if(action == "music.getAlbum"): #get song play a single song
        fullfill_text=play_album(param)
        tp = "music"
    #if user is action weatherjjjj
    if(action == "weather"): #get the next 5 day forcast of this city
        fullfill_text=process_weather(param)
        tp = "weather"
    #ligths control
    if(action == "IOT.turn_on"):
        status = light_control("on") #turn on the light
        if(status == 207):
            fullfill_text="Lights are now on!"
        else:
            fullfill_text = "Error turning on the light code: " + str(status)
    if(action == "IOT.turn_off"):
        status = light_control("off") #turn on the light
        if(status == 207):
            fullfill_text="Lights are now off!"
        else:
            fullfill_text = "Error turning off the light code: " + str(status)
    #other functions to fullfill

    #if until this stage fullfill_text still not being filled means not recognised intend retunr error to user
    if(not fullfill_text):
        fullfill_text = "Sorry I do not understand what you said!"

    #processing complete sedn the result to the front end
    print("final fullfill text:",fullfill_text,type(fullfill_text))
    res=  {'ObjectID': object_id, 'res': fullfill_text,'type':tp}
    print("the response is:" ,res)

    #return res
    res = json.dumps(res)
    return jsonify(res) 

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))
    app.run(debug=True)
    #app.run()
'''
#============================================================================
#socket version
#set up the socket listening to the cient request
args = sys.argv[1:] #python 8888 5555
ip =  "127.0.0.1"
port = int(args[0])
print(ip)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((str(ip), port))
s.listen()
conn, addr = s.accept()

with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if data: #if there is any data from the front end
            print("received:",data.decode())

            #pass the user text to the dialogflow api
            #music_flag if there is conent stores the parametres

            context_client, parent,param,action,fullfill_text = detect_intent_texts(project_id,session_id,[data],"en-US")
            print("action:",action)
            print("fullfilltext:",fullfill_text)

            #return list of context
            for element in context_client.list_contexts(parent):
                print("context elements:",element)


            #context_client.delete_all_contexts(parent) 

            tp = 'text' #type init as text
            if(fullfill_text): #if there is response means not the end asking for params so pass as text
                print(fullfill_text,type(fullfill_text),"type:",tp)
                conn.send("do not understand".encode() if not fullfill_text else fullfill_text.encode())
                continue
                #return res
            
            #here means the final process , to fullfill in the backend
            if(action == "music.getSongsByArtist"): 
                fullfill_text=artist_song(param)
                tp ="music"
            if(action == "music.getAlbumListByArtist"):
                fullfill_text=artist_album(param)
                tp ="music"
            if(action == "music.playSong"):
                fullfill_text=play_song(param)
                tp = "music"

            #if user is action weather
            if(action == "weather"): #get the next 5 day forcast of this city
                fullfill_text=process_weather(param)
                tp = "weather"
            if(action == "IOT.turn_on"):
               light_control("on") #turn on the light
               fullfill_text="Lights are now on!"
            if(action == "IOT.turn_off"):
               light_control("off") #turn on the light
               fullfill_text="Lights are now off!"

          
            #processing complete sedn the result to the front end
            print(fullfill_text,type(fullfill_text),"type:",tp)
            fullfill_text = json.dumps(fullfill_text) #stringify as json 

            conn.send("do not understand".encode() if not fullfill_text else fullfill_text.encode())
s.close()

