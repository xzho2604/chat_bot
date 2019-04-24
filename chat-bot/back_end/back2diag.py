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
#from api_service.light.light_control import *
import random
from helper import *
import re

from database.userservice import *
import pickle
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
from google.protobuf.struct_pb2 import Struct, Value



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
#get the project id from google cloud of the dialogflow agent
project_id = 'weather-f22a9'  
session_id = 'first'  #API caller defined

#set up session client
session_client = dialogflow.SessionsClient()
session = session_client.session_path(project_id, session_id)
print('Session path: {}\n'.format(session))

#set up context client to manipulate context
context_client = dialogflow.ContextsClient()
parent = context_client.session_path(project_id, session_id)

#============================================================================
#function to pass input and get back the response
def detect_intent_texts(text, language_code):

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
   
    return param, action ,fulfillment
    #print(response)

#------------------------------------------------------------------------------
#given user id will reload the user context 
def load_user_context(userid):
    new_context = get_context(str(userid))
    if new_context == "":
        return False

    context_list = pickle.loads(new_context) #change string to list  
    for s in context_list:
        data = json.loads(s) #make each context string to json
        name = data["name"]
        life = data["lifespanCount"]

        #create a template context class
        temp = {"name":name,"lifespan_count":life} #a template to create context
        blank = context_client.create_context(parent,temp) #create a black context
        context_client.delete_context(name) #delte the previous temp
        
        #restore the context
        restore = Parse(s,blank)
        result = context_client.create_context(parent,restore) #create a black context

    return True
#------------------------------------------------------------------------------
def save_user_context(userid):
    context_list = []#google.cloud.dialogflow_v2.types.Context
    for e in context_client.list_contexts(parent): 
        print("====================================")
        print("Active Context:")
        print(e)

        pay_text = MessageToJson(e) #change the google class to string
        context_list.append(pay_text)


    #now serilise the list and save to databse
    s_list = pickle.dumps(context_list) #list serilisable
    update_user(str(userid),"content",s_list) #save the context to databse

    print("now contexts saved to the databse:")
    print(s_list)
    

#------------------------------------------------------------------------------
def music():
    subprocess.call("python ./api_service/music/web-api-auth/authorization_code/auto_login.py",shell = True)
#============================================================================
app = Flask(__name__)

#the thread to start
spotify = threading.Thread(target = music)
#---------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login(): #the front end signal user log in retrive the user context from data base if there is any
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason
    print(req)
    params = req['params']
    #user = params["user"] #user is of struct {userID:id, userName:name}
    user_id = params["userID"]

    #clear the current context if there is any
    context_client.delete_all_contexts(parent)

    #with user_id get the context from the databse if there is any
    result = load_user_context(user_id)
    print("now load all the previous user context and login")

    #print out all restored context
    for e in context_client.list_contexts(parent):
        print("-------------------------------------")
        print("Restored Context:")
        print(e)
    
    spotify.start() #auto login user spotify account

    return jsonify({"logged_in":True}),200

#---------------------------------------------------------------------------
@app.route('/logout', methods=['POST'])
def logout(): #front end signal user log off save the user context to the databse 
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason
    #print(req)
    params = req['params']
    user_id = params["userID"]

    save_user_context(userid) #save the current active context to databse

    #stop the spotify thread
    #spotify.stop()

    return jsonify({"logged_in":True}),200

#---------------------------------------------------------------------------
#return to the fron end json:id,text,type
@app.route('/', methods=['POST'])
#@app.route('/', methods=['GET'])
def backend():
    #extrac the relevant parametrs from the front end 
    req = request.get_json(silent=True, force=True) #req is a dict of returned jason
    print(req)
    params = req['params']
    query_id= params['queryID'] #objectID change to query id
    query = params['msg']
    user = params["userID"] #user is of struct {userID:id, userName:name}
    print("query:",query)
    
    param,action,fullfill_text = detect_intent_texts(query,"en-US")
    #print("action:",action)
    #print("fullfilltext:",fullfill_text)
    
    #the response to the front end would be
    #res=  {'queryID': query_id, 'res': fullfill_text,'type':"text","user"":user}

    tp = 'text' #type init as text
    if(fullfill_text): #if there is response means not the end asking for params so pass as text
        print(fullfill_text,type(fullfill_text),"type:",tp)
        res=  {'queryID': query_id, 'res': fullfill_text,'type':"text",'user':user}
        res = json.dumps(res)
        return jsonify(res)
    
    #here means the final process , to fullfill in the backend
    if(action == "music.getSongsByArtist"): #get artist return a recomended song
        fullfill_text=artist_song(param)
        tp ="music"
        if(fullfill_text == ""):
            fullfill_text = "The Spotify token expired please refresh!"
            tp = "text"
    if(action == "music.getAlbumListByArtist"): #get artist return an album
        fullfill_text=artist_album(param)
        tp ="music"
        if(fullfill_text == ""):
            fullfill_text = "The Spotify token expired please refresh!"
            tp = "text"
    if(action == "music.playSong"): #get song play a single song
        fullfill_text=play_song(param)
        tp = "music"
        if(fullfill_text == ""):
            fullfill_text = "The Spotify token expired please refresh!"
            tp = "text"
    if(action == "music.getAlbum"): #get song play a single song
        fullfill_text=play_album(param)
        tp = "music"
        if(fullfill_text == ""):
            fullfill_text = "The Spotify token expired please refresh!"
            tp = "text"
    #if user is action weatherjjjj
    if(action == "weather"): #get the next 5 day forcast of this city
        fullfill_text=process_weather(param)
        tp = "weather"
        if(fullfill_text["weather"] == ""): #weather not within the range
            fullfill_text = "Sorry, Only 5 days weatehr forcast is available"
            tp = "text"
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
    res=  {'queryID': query_id, 'res': fullfill_text,'type':tp,'user':user}
    print("the response is:" ,res)

    #return res
    res = json.dumps(res)
    return jsonify(res) 

if __name__ == '__main__':
    app.run(debug=True,port=8000)

