import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (os.getenv('MONGO_USERNAME'), os.getenv('MONGO_PASSWORD'))
    DATABASE = None
    PAGE_SIZE = 12

    def initialize():
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        Database.DATABASE = client['news']
