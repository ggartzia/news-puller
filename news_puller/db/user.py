import logging
import pymongo
from news_puller.database import Database

user_db = Database.DATABASE['users']

def save_user(user):
    try:
        user_db.update_one({'_id': user['id']},
                           {'$setOnInsert': user,
                           '$inc':{'tweets': 1}},
                           upsert=True)

    except Exception as e:
        logging.error('There was an error while trying to save user: %s, %s', user, e)


def search_user(name):
    user = None

    try:
        user = user_db.find_one({'screen_name': name})

    except Exception as e:
        logging.error('There was an error fetching user: %s. %s', name,  e)

    return user


def select_users(page):
    size = 3 * Database.PAGE_SIZE

    total = user_db.count_documents({})

    users = user_db.find({},
                         sort=[('tweets', pymongo.DESCENDING)]).skip(page * size).limit(size)

    return {'total': total,
            'items': list(users)}