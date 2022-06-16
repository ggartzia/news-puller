from time import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_gzip import Gzip
from news_puller.twitter import TweetListener
import news_puller.db.new as db_news
import news_puller.db.topic as db_topics
import news_puller.db.user as db_users
import news_puller.db.tweet as db_tweets

start_time = int(time())

app = Flask(__name__)
cors = CORS(app)
Gzip(app)

# Start background jobs
TweetListener()


@app.route('/', methods=['GET'])
def health_check():
    response = {
        'overallStatus': 'OK',
        'version': 1,
        'startTime': start_time
    }
    return jsonify(response)


@app.route('/get/<theme>/<int:since>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_last_news(theme, since, page):
    news = db_news.select_last_news(since, theme, page)

    return jsonify(news)


@app.route('/get/trending/<int:since>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_trending_news(since, page):
    news = db_news.select_trending_news(since, page)

    return jsonify(news)


@app.route('/get/news/<topic>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_topic_news(topic, page):
    news = db_news.select_topic_news(topic, page)

    return jsonify(news)


@app.route('/get/related/<id>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_related_news(id, page):
    news = db_news.select_related_news(id, page)

    return jsonify(news)


@app.route('/get/topics/<theme>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_topics(theme, page):
    topics = db_topics.select_topics(theme, page)

    return jsonify(topics)


@app.route('/get/media/<theme>', methods=['GET'])
@cross_origin()
def fetch_media(theme):
    media = db_news.select_media_stats(theme)

    return jsonify(media)


@app.route('/get/media/<media>/news/page/<int:page>', methods=['GET'])
@cross_origin()
def fetch_media_news(media, page):
    news = db_news.select_media_news(media, page)

    return jsonify(news)


@app.route('/get/users/page/<int:page>', methods=['GET'])
@cross_origin()
def fetch_users(page):
    users = db_users.select_users(page)

    return jsonify(users)


@app.route('/get/tweets/<id>', methods=['GET'])
@cross_origin()
def get_all_tweets(id):
    all_tweets = db_tweets.select_all_tweets(id)
    new = db_news.search_new(id)

    return jsonify({'new': new,
                    'total': new['total'],
                    'chart': all_tweets})


@app.route('/get/tweets/<id>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_tweets(id, page):
    tweets = db_tweets.select_tweets(id, None, page)

    return jsonify(tweets)


@app.route('/get/tweets/user/<userName>/page/<int:page>', methods=['GET'])
@cross_origin()
def fetch_user_tweets(userName, page):
    user = db_users.search_user(userName)
    tweets = db_tweets.select_tweets(None, user['id'], page) 

    return jsonify({'total': db_tweets.count_user_tweets(user['id']),
                    'user': user,
                    'items': tweets})
