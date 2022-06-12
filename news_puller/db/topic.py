from logging import getLogger, DEBUG
import pymongo
from news_puller.database import Database

topic_db = Database.DATABASE['topics']

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


def save_topics(topics, theme):
    for topic in topics:
        topic_db.update_one({'name': topic, 'theme': theme}, {'$inc': {'usage': 1}},
                            upsert=True)


def select_topics(theme, page):
    size = 4 * Database.PAGE_SIZE

    total = topic_db.count_documents({'theme': theme})
    
    topics = topic_db.find({'theme': theme}, {'_id': 0},
                           sort=[('usage', pymongo.DESCENDING)]).skip(page * size).limit(size)

    return {'total': total,
            'items': list(topics)}
