# capstone-project-mr-robot

* implement Book room or trip using diagflow
* Try backend API with Json file
* import Airline Modul or coffe module to implement simple booking for order function
## WorkSpaces:
* [Project Proposal](https://www.overleaf.com/5973716318hnyngfttwfyj)
## BackEnd Usage:
* cd chat-bot/back_end
* python back2dialogflow.py
* In another terminal:
```bash
ssh -R chabot:80:localhost:8000 serveo.net 
```
Then your local host can be access via static ip address of: <br /><br />
https://chatbot.serveo.net/


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
https://stackoverflow.com/questions/50217133/dialogflow-detectintenttext

## Music api (spotify) calling process:
* cd ..\capstone-project-mr-robot\chat-bot\back_end\api_service\music\web-api-auth\authorization_code
* node app.js
* visit localhsot:8888 and log in with a spotify account then the token will be stored in local program automatically
