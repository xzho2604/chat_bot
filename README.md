# capstone-project-mr-robot
## FrontEnd Usage:
* make sure you have nodejs installed in your system
* cd chat-bot/chat-front-end
* (Run this command only at the first time: ) npm install
* npm start

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

