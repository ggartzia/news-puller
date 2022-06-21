import os
import pymongo
from dotenv import load_dotenv


load_dotenv()


class Database(object):
    usr = os.getenv('MONGO_USERNAME')
    paw = os.getenv('MONGO_PASSWORD')
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (usr, psw)

    client = pymongo.MongoClient(URI)  # establish connection with database
    DATABASE = client['news']

    PAGE_SIZE = 12

