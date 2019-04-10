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
    data = {"pickle":user["pickle"], "image":user["image"]}
    print(data)
    return data

def update_user(user_name, field_name, value):
    if field_name == "pickle":
        myquery = {"name":user_name}
        newvalues = { "$set": { "pickle": value }}
        collection.update_one(myquery, newvalues)
    elif field_name == "image":
        myquery = {"name":user_name}
        newvalues = { "$set": { "image": value }}
        collection.update_one(myquery, newvalues)

if __name__ == "__main__":

    get_user("eric")
    update_user("eric", "pickle", "pickle_1")
    get_user("eric")
    update_user("eric", "image", "address_1")
    get_user("eric")
