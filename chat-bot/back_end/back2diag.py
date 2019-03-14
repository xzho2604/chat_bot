'''
Set up the key for authentication
Google Cloud:
1.IAM & Admin -> Roles-> add dialogflow roles and permissions
2.service account -> create service account -> add role and permission
2. API Services -> Crendentials -> create crednetials -> service account ->jason key
3. add os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'yourfilename.json' to tbe file to run
'''
import os
import dialogflow
import sys
import socket

#============================================================================
#dialogflow client api config
#get access to the service key each service account has its key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account_key/weather_key.json'

#function to pass input and get back the response
def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        
        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text
        #print(response)

#get the project id from google cloud of the dialogflow agent
project_id = 'weather-f22a9'  
session_id = 'first'  #API caller defined
#============================================================================
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
            fullfill_text = detect_intent_texts(project_id,session_id,[data],"en-US")
            conn.send("do not understand".encode() if not fullfill_text else fullfill_text.encode())
s.close()


