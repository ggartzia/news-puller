from logging import getLogger, DEBUG
import pymongo
from news_puller.db import Database

topic_db = Database.DATABASE['topics']

def update_topic(topic, theme, saved_topics):
    if topic not in saved_topics:
        updateResult = topic_db.update_one({'name': topic, 'theme': theme}, {'$inc': {'usage': 1}})
        return (updateResult.modified_count == 1)
    return True


def save_topics(topics, theme):
    saved_topics = []

    try:
        for t in topics:
            new_topics = []

            # Calculate only two words topics, if the two word topic exists in the DB, count and move on
            if Database.update_topic(t, theme, saved_topics):
                new_topics.append(t)
            else:
                # If it does not exist, split the topic, if one or both exists count.
                words = t.split()
                for w in words:
                    if Database.update_topic(w, theme, saved_topics):
                        new_topics.append(w)
                
                # If none of them exist, save the three of them.
                if not new_topics:
                    new_topics = [t] + words
                    topic_db.insert_many([{'name': nt, 'theme': theme, 'usage': 1} for nt in new_topics])

            # Return only the topics saved
            saved_topics += new_topics
            saved_topics = list(dict.fromkeys(saved_topics))

            # Save only the first 10 or 12 topics
            if len(saved_topics) > 10:
                break

    except Exception as e:
        logger.error('There was an error while trying to save topics: %s', e)

    return saved_topics


def select_topics(theme, page):
    size = 4 * Database.PAGE_SIZE

    topics = topic_db.find({'theme': theme}, {'_id': 0},
                           sort=[('usage', pymongo.DESCENDING)]).skip(page * size).limit(size)

    return list(topics)


def update_topics(new, limit=3):
    topics = topic_db.find({'name': {'$in': new['topics']}, 'theme': new['theme']},
                           {'_id': 0},
                           sort=[('usage', pymongo.DESCENDING)]).limit(limit)
    new['topics'] = list(topics)
    
    return new