from logging import getLogger, DEBUG
import pymongo
from news_puller.database import Database

user_db = Database.DATABASE['users']

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

def save_user(user):
    try:
        user_db.update_one({'_id': user['id']},
                           {'$setOnInsert': user,
                           '$inc':{'tweets': 1}},
                           upsert=True)

    except Exception as e:
        logger.error('There was an error while trying to save user: %s, %s', user, e)


def search_user(id):
    user = None

    try:
        user = user_db.find_one({'_id': id})

    except Exception as e:
        logger.error('There was an error fetching user: %s. %s', id,  e)

    return user


def select_users(page):
    size = 3 * Database.PAGE_SIZE

    users = user_db.find({},
                         sort=[('tweets', pymongo.DESCENDING)]).skip(page * size).limit(size)

    return list(users)