import pymongo
from pymongo import MongoClient
client=MongoClient("localhost",27017)
db = client["chatbot"]
collection = db["users"]

def show():
    for x in collection.find():
        print(x)

def get_user(user_name):
    user = collection.find_one({"name":user_name})
    print(user["content"])
    data = {"pickle":user["pickle"], "image":user["image"]}
    print(data)
    return data

def get_context(user_name):
    user = collection.find_one({"name":user_name})
    return user["content"]




def update_user(user_name, field_name, value):
    myquery = {"name":user_name}
    newvalues = { "$set": { field_name: value }}
    collection.update_one(myquery, newvalues)



if __name__ == "__main__":
    #string = "name: \"projects/weather-f22a9/agent/sessions/first/contexts/lights\"\nlifespan_count: 5\nparameters {\nfields {\nkey: \"device\"\nvalue {\nstring_value: \"light bulb\"\n}\n}\nfields {\nkey: \"device.original\"\nvalue {\nstring_value: \"light\"\n}\n}\nfields {\nkey: \"intent_action\"\nvalue {\nstring_value: \"IOT.turn_on\"\n}\n}\n}"
    string = 'context'
    show()
    print(string)
    get_user("eric")
    update_user("eric", "pickle", "pickle_1")
    get_user("eric")
    update_user("eric", "content", string)
    get_user("eric")
