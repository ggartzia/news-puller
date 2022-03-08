import re
import news_puller.config as cfg
from datetime import datetime, timedelta
from logging import getLogger, DEBUG
import pymongo


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (cfg.MONGO_USERNAME, cfg.MONGO_PASSWORD)
    DATABASE = None
    PAGE_SIZE = 12

    def initialize():
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        Database.DATABASE = client['news']


    def save_new(new):
        try:
            mongo_db = Database.DATABASE['news']
            mongo_db.update_one({'_id': new['id']}, {'$set': new}, upsert=True)

        except Exception as e:
            logger.error('There was an error while trying to save new: %s, %s', new, e)


    def update_topic(mongo_db, topic, theme, saved_topics):
        print("Topics saved so far", saved_topics)
        if topic not in saved_topics:
            updateResult = mongo_db.update_one({'name': topic, 'theme': theme}, {'$inc': {'tweets': 1}})
            return (updateResult.modified_count == 1)
        return True


    def save_topics(topics, theme):
        print("Start topics", topics)
        saved_topics = []
        mongo_db = Database.DATABASE['topics']

        try:
            for t in topics:
                new_topics = []

                # Calculate only two words topics, if the two word topic exists in the DB, count and move on
                if Database.update_topic(mongo_db, t, theme, saved_topics):
                    new_topics.append(t)
                else:
                    # If it does not exist, split the topic, if one or both exists count.
                    words = t.split()
                    for w in words:
                        if Database.update_topic(mongo_db, w, theme, saved_topics):
                            new_topics.append(w)
                    
                    # If none of them exist, save the three of them.
                    if not new_topics:
                        new_topics = [t] + words
                        mongo_db.insert_many([{'name': nt, 'theme': theme, 'tweets': 1} for nt in new_topics])

                # Return only the topics saved
                saved_topics += new_topics

        except Exception as e:
            logger.error('There was an error while trying to save topics: %s', e)
        print("End topics", saved_topics)
        return saved_topics


    def save_tweets(tweets):
        try:
            if tweets:
              mongo_db = Database.DATABASE['tweets']
              mongo_db.insert_many(tweets, ordered = False)
            
        except Exception as e:
            logger.error('There was an error while trying to save tweets: %s', e)


    def save_user(user):
        try:
            mongo_db = Database.DATABASE['users']
            mongo_db.update_one({'_id': user['id']}, {'$setOnInsert': user , '$inc':{'tweets': 1}}, upsert=True)

        except Exception as e:
            logger.error('There was an error while trying to save user: %s, %s', user, e)


    def search_new(id):
        new = None
        
        try:
            mongo_db = Database.DATABASE['news']
            new = mongo_db.find_one({'_id': id})
        except Exception as e:
            logger.error('There was an error fetching the data: %s', e)
            
        return new


    def update_topics(new):
        mongo_db = Database.DATABASE['topics']
        topics = mongo_db.find({'name': {'$in': new['topics']}, 'theme': new['theme']},
                               {'_id': 0},
                               sort=[('usage', pymongo.DESCENDING)]).limit(5)
        
        new['topics'] = list(topics)
        
        return new


    def select_last_news(hour, theme, page):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)

        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)},
                              'theme' : theme}, {'_id': 0 },
                             sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        news = map(Database.update_topics, list(news))

        return list(news)


    def select_trending_news(hour, page):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)

        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}}, {'_id': 0 },
                             sort=[('tweetCount', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        
        return list(news)


    def select_topic_news(topic, page):
        mongo_db = Database.DATABASE['news']
        
        news = mongo_db.find({'topics': topic},
                             sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)


    def select_related_news(id, page):
        mongo_db = Database.DATABASE['news']
        main_new = Database.search_new(id)

        if main_new:
            news = mongo_db.find({'topics': {'$all': main_new['topics']}},
                                 sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news) 


    def select_topics(theme, limit):
        mongo_db = Database.DATABASE['topics']
        
        topics = mongo_db.find({'theme': theme}, {'_id': 0 },
                               sort=[('usage', pymongo.DESCENDING)]).limit(limit)

        return list(topics)


    def select_tweets(new, page):
        mongo_db = Database.DATABASE['tweets']

        news = mongo_db.find({'new': new},
                             sort=[('created_at', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)
    

    def num_news(paper, theme):
        mongo_db = Database.DATABASE['news']
        
        return mongo_db.count_documents({'paper': paper, 'theme': theme})


    def last_new(paper, theme):
        mongo_db = Database.DATABASE['news']
        new = mongo_db.find_one({'paper' : paper, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])
        
        if new is None:
            return None
        else:
            return new['published']

    def num_tweets(new):
        mongo_db = Database.DATABASE['tweets']
        
        return mongo_db.count_documents({'new': new})
