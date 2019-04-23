# capstone-project-mr-robot

* implement Book room or trip using diagflow
* Try backend API with Json file
* import Airline Modul or coffe module to implement simple booking for order function
## WorkSpaces:
* [Project Proposal](https://www.overleaf.com/5973716318hnyngfttwfyj)
## BackEnd Usage:
* cd chat-bot/back_end
* conda activate ass2 (To run in this env)
* python back2dialogflow.py
* In another terminal:
run ./ngrok http 5000


* cd chat-bot/back_end/face/network_imgage.py
* conda activate carND-term1 (TO opencv env)
* python network_image.py -d face_detection_model -r output/recognizer.pickle -l output/le.pickle

### Env Set up
* To Export and create an env with .yml:
```shell
conda env export > environment.yml
conda env create -f environment.yml
```



## FrontEnd Usage:
* make sure you have nodejs installed in your system
* cd chat-bot/chat-front-end
* (Run this command only at the first time: ) npm install
* npm start

## Resources:
* Diagflow Basic Tutorial: <br />
  https://medium.com/swlh/how-to-build-a-chatbot-with-dialog-flow-chapter-4-external-api-for-fulfilment-3ab934fd7a00 <br />
  https://www.youtube.com/watch?v=-tOamKtmxdY
* Build Local Chat Bot Model Using Python: <br />
  https://www.analyticsvidhya.com/blog/2018/01/faq-chatbots-the-future-of-information-searching/
* Use Python Diagflow API example: <br />
  https://pusher.com/tutorials/chatbot-flask-dialogflow  <br />
  https://www.youtube.com/watch?v=qd-3D2USCw0
* Diagflow Python Client API: <br />
  https://dialogflow-python-client-v2.readthedocs.io/en/latest/
  https://developers.google.com/api-client-library/python/apis/dialogflow/v2 <br />
* Report Chart Drawing: <br />
  www.lucidchart.com/
* Read Python API:<br />
  https://cloud.google.com/dialogflow-enterprise/docs/quickstart-api <br />
* Front End link with back  <br />
https://alligator.io/react/axios-react/<br />
* Back End to Diagflow API configure<br />
https://stackoverflow.com/questions/50217133/dialogflow-detectintenttext<br />
* Smart Light API<br />
https://api.developer.lifx.com/docs/set-state<br />
* Python context switch<br />
https://flask-assistant.readthedocs.io/en/latest/contexts.html<br />
https://dialogflow-python-client-v2.readthedocs.io/en/latest/gapic/v2/api.html<br />

## Music api (spotify) calling process:
* cd ..\capstone-project-mr-robot\chat-bot\back_end\api_service\music\web-api-auth\authorization_code
* node app.js
* visit localhsot:8888 and log in with a spotify account then the token will be stored in local program automatically

## Mongodb init:
* brew install mongodb
* run 'mongod -dbpath ../chat-bot/back_end/database/data/db2' to init the database data and service at "localhost:27017"
* run 'mongoimport -d chatbot -c users --file ../data/users.json' to import the data into database
* import userservice.py to call the functions
