from logging import getLogger, DEBUG
import pymongo
from news_puller.database import Database

comment_db = Database.DATABASE['comments']

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

def save_comment(comm):
    try:
        comment_db.insert_one(comm)

    except Exception as e:
        logger.error('There was an error while trying to save comment: %s, %s', comm, e)

