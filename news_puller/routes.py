from time import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_gzip import Gzip
from news_puller.fetch import get_news
from news_puller.media import get_media
from news_puller.database import Database
import news_puller.db.new as db_news
import news_puller.db.media as db_media
import news_puller.db.topic as db_topics
import news_puller.db.user as db_users
import news_puller.db.tweet as db_tweets

start_time = int(time())

app = Flask(__name__)
cors = CORS(app)
Gzip(app)


@app.route('/', methods=['GET'])
def health_check():
    response = {
        'overallStatus': 'OK',
        'version': 1,
        'startTime': start_time
    }
    return jsonify(response)


@app.route('/fetch/<media>', methods=['GET'])
def fetch_news(media):
    get_news(media)

    return 'OK'


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


@app.route('/get/related/<id>', methods=['GET'])
@cross_origin()
def get_related_news(id):
    news = db_news.select_related_news(id)

    return jsonify(news)


@app.route('/get/topics/<theme>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_topics(theme, page):
    topics = db_topics.select_topics(theme, page)

    return jsonify(topics)


@app.route('/get/media/<theme>', methods=['GET'])
@cross_origin()
def fetch_media(theme):
    media = get_media(theme)

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


@app.route('/get/tweets/<id>/page/<int:page>', methods=['GET'])
@cross_origin()
def get_tweets(id, page):
    tweets = db_tweets.select_tweets(id, page)

    return jsonify(tweets)


@app.route('/get/tweets/user/<int:user>/page/<int:page>', methods=['GET'])
@cross_origin()
def fetch_user_tweets(user, page):
    tweets = db_tweets.select_user_tweets(user, page)

    return jsonify(tweets)
