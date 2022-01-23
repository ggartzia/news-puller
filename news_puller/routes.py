from time import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_gzip import Gzip
from news_puller.fetch import get_news
from news_puller.media import get_media
from news_puller.db import Database
import news_puller.scheduler


start_time = int(time())

app = Flask(__name__)
cors = CORS(app)
Gzip(app)

Database.initialize()

@app.route('/_health/pool', methods=['GET'])
def health_pool():
    return 'OK'


@app.route('/_health/check', methods=['GET'])
def health_check():
    response = {
        'overallStatus': 0,
        'version': 1,
        'startTime': start_time
    }
    return jsonify(response)


@app.route('/', methods=['GET'])
def index():
    news = Database.select_last_news(24, 'noticias')
    return jsonify(news)


@app.route('/fetch/<media>', methods=['GET'])
def fetch_news(media):
    news = get_news(media)

    return jsonify(news)


@app.route('/get/<theme>/<int:since>', methods=['GET'])
@cross_origin()
def get_last_news(theme, since):
    news = Database.select_last_news(since, theme)

    return jsonify(news)


@app.route('/get/trending/<int:since>', methods=['GET'])
@cross_origin()
def get_trending_news(since):
    news = Database.select_trending_news(since)

    return jsonify(news)


@app.route('/get/news/<topic>', methods=['GET'])
@cross_origin()
def get_topic_news(topic):
    news = Database.select_topic_news(topic)

    return jsonify(news)


@app.route('/get/new/<id>', methods=['GET'])
@cross_origin()
def get_new(id):
    new = Database.search_new(id)

    return jsonify(new)


@app.route('/get/relatedNews/<id>', methods=['GET'])
@cross_origin()
def get_related_news(id):
    news = Database.select_related_news(id)

    return jsonify(news)


@app.route('/get/topics/<theme>', methods=['GET'])
@cross_origin()
def get_topics(theme):
    topics = Database.select_topics(theme, 50)

    return jsonify(topics)


@app.route('/get/media/<theme>', methods=['GET'])
@cross_origin()
def fetch_media(theme):
    media = get_media(theme)

    return jsonify(media)


@app.route('/get/tweets/<id>', methods=['GET'])
@cross_origin()
def get_tweets(id):
    tweets = Database.select_tweets(id)

    return jsonify(tweets)

