import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (os.getenv('MONGO_USERNAME'), os.getenv('MONGO_PASSWORD'))
    client = pymongo.MongoClient(Database.URI)  # establish connection with database
    DATABASE = client['news']
    
    PAGE_SIZE = 12
