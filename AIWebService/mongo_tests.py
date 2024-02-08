# Connect to my Mongo instance at the database gpt-tests and the collecction Messages: 
# mongo "mongodb+srv://cluster0.7jx1p.mongodb.net/gpt-tests" --username admin
from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient(os.environ['MONGO_URL'])
# Set the db object to point to the business database
db=client.get_database('gpt-tests')
# Set the collection object to point to the businesses collection
messageCollection=db.Messages


# ADD DATA
# add a sample test document to the database

# doc = {'role': 'user', "content": "Hello, I am a user"}
# messageCollection.insert_one(doc)


# VIEW DATA
# print the documents in the collection


# for doc in messageCollection.find():
#     pprint(doc)


# MAKE A FUNCTION THAT WILL RETURN THE MESSAGES
def get_messages():
    messages = []
    for doc in messageCollection.find():
        doc = {"role": doc["role"], "content": doc["content"]}
        messages.append(doc)
    return messages

def add_message(role, content):
    doc = {'role': role, "content": content}
    messageCollection.insert_one(doc)
    return "Message added"