# Smart-house-bulter-chat-bot
That is able to control IOT devices like lights , vacum cleaner , auto dog feeder and other serivices like spotify to play music and open weather to enquiry weather.Using google dialogflow as NLP to produce human like smmooth converstation
## FrontEnd Usage:
* make sure you have nodejs installed in your system
* cd chat-bot/chat-front-end
* (Run this command only at the first time: ) npm install
* npm start

## Backend: 
* Backend will be running in aws ,so if you want to test our system please let me know in advance so that I can start the 
Backend server on aws
## Mongodb init:
* brew install mongodb
* run to init the database data and service at "localhost:27017"
```shell
mongod -dbpath ./db2
```
* run to import the data into database
```shell
mongoimport -d chatbot -c users --file ./data/users.json
```

