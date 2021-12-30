import re
import news_puller.config as cfg
from datetime import datetime, timedelta
from math import log
from logging import getLogger, DEBUG
import pymongo

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
sw = stopwords.words('spanish')


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (cfg.MONGO_USERNAME, cfg.MONGO_PASSWORD)
    DATABASE = None

    def initialize():
        print('Connect with ' + Database.URI)
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        print('Connection done')
        Database.DATABASE = client['news']


    def calculate_idf(num_docs, theme, title):
        topics = []
        
        try:
            idfs = {}
            
            title = title.lower()
            title = re.sub("[^a-zñçáéíóú]", " ", title)
            
            for term in title.split():
                if term not in sw:
                    print("Convertir la palabra " + term + " en ")
                    term = stemmer.stem(term)
                    print(term)
                    # Use the number of docs that contain the term to calculate the IDF
                    term_docs = Database.DATABASE['news'].count_documents({'theme': theme, 'title' : {'$regex' : term}})
                    idfs[term] = log((num_docs - term_docs + 0.5) / (term_docs + 0.5))

            idfs = {k: v for k, v in idfs.items() if v > cfg.TF_IDF_MIN_WEIGHT}
            
            topics = list(idfs.keys())
        
        except Exception as e:
            logger.error(e)
            
        return topics[:3]


    def save_news(news):
        try:
            print('Save ' + str(len(news)) + ' news in MONGO')
            
            mongo_db = Database.DATABASE['news']

            result = mongo_db.bulk_write([pymongo.UpdateOne({'_id': n['_id']}, {"$set": n}, upsert=True) for n in news])
            #mongo_db.insert_many(news, ordered = False)
            print(result.bulk_api_result)

        except Exception as e:
            logger.error(e)
            logger.error('There was an error while trying to save news')


    def update(id, tweetCount):
        try:
            print('Update ' + id + ' new in MONGO')
            
            mongo_db = Database.DATABASE['news']
            mongo_db.update_one({ '_id': id }, { "$set": { 'tweetCount': tweetCount } })
            
        except Exception as e:
            logger.error(e)
            logger.error('There was an error while trying to update the new')


    def search_new(id):
        new = None
        
        try:
            print('Get ' + str(id) + ' new in MONGO')
            mongo_db = Database.DATABASE['news']
            new = mongo_db.find_one({'_id': id})
        except:
            logger.error('There was an error fetching the data')
            
        return new


    def select_last_news(hour, theme):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        print('Return last ' + str(hour) + ' hours news in MONGO')
        
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)},
                              'theme' : theme},
                             sort=[('published', pymongo.DESCENDING)])
                       .limit(100)

        return list(news)


    def select_day_news(day, theme, order):
        fromDay = datetime.now() - timedelta(days = (day - 1))
        toDay = datetime.now() - timedelta(days = day)
        print('Return news from ' + str(fromDay) + ' to ' + str(toDay) + ' hours news in MONGO')

        mongo_db = Database.DATABASE['news']

        orderBy = pymongo.DESCENDING
        if (order == 1) : orderBy = pymongo.ASCENDING

        news = mongo_db.find({'published': {'$gte': str(fromDay), '$lte': str(toDay)},
                              'theme' : theme},
                             sort=[('published', orderBy)])

        return list(news)


    def select_trending_news(hour):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        print('Return trending news in the last ' + str(hour) + ' hours in MONGO')

        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}},
                             sort=[('tweetCount', pymongo.DESCENDING)])
                       .limit(100)

        return list(news)


    def select_topic_news(topic):
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'topics': topic},
                             sort=[('published', pymongo.DESCENDING)])
                       .limit(100)

        return list(news)


    def select_topics(hour):
        mongo_db = Database.DATABASE['news']
        last_hour_date_time = datetime.now() - timedelta(hours = hour)

        mongo_db = Database.DATABASE['news']
        topics = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}}).distinct('topics')

        news_by_topic = map(lambda t: {'name': t,
                                       'numNews': mongo_db.count_documents({'topics': t})},
                            topics)

        sorted_topics = sorted(news_by_topic, key = lambda t: t['numNews'])

        return sorted_topics[:100]


    def num_news(media, theme):
        print('Return the number of documets in MONGO')

        filter = {}
        if media : 
            filter['paper'] = media
            
        if theme : 
            filter['theme'] = theme
        
        print('Filter by ' + str(filter))
        
        mongo_db = Database.DATABASE['news']
        num = mongo_db.count_documents(filter)
        
        return num


    def last_new(media, theme):
        print('Return last fetched new from ' + media + ' from theme ' + theme + ' in MONGO')
        
        mongo_db = Database.DATABASE['news']

        new = mongo_db.find_one({'paper' : media, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])

        return new['published']
