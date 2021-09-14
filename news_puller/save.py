from dotenv import load_dotenv
import os
import pymongo

load_dotenv()  # use dotenv to hide sensitive credential as environment variables

DATABASE_URL = f'mongodb+srv://{os.environ.get("mongo-user")}:{os.environ.get("mongo-password")}'\
               f'@{os.environ.get("mongo-cluster")}/{os.environ.get("mongo-db")}?'\
               'retryWrites=true&w=majority'  # get connection url from environment

client = pymongo.MongoClient(DATABASE_URL)  # establish connection with database
mongo_db = client.db  # assign database to mongo_db
mongo_db.launches.drop()  # clear the collection


def save(news):

    mongo_db.launches.insert_many(news)
