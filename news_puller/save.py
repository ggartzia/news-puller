from dotenv import load_dotenv
import json
import os
import pymongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables

DATABASE_URL = f'mongodb+srv://{os.environ.get("mongo-user")}:{os.environ.get("mongo-password")}'\
               f'@{os.environ.get("mongo-cluster")}/{os.environ.get("mongo-db")}?'\
               'retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database
mongo_db = client.db  # assign database to mongo_db
mongo_db.launches.drop()  # clear the collection

with open('static/data/launches.json') as file:  # opening the json file
    file_data = json.load(file)

if isinstance(file_data, list):
    mongo_db.launches.insert_many(file_data)  # if data is a list
else:
    mongo_db.launches.insert_one(file_data)  # if data is a document object
