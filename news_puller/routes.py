from time import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_gzip import Gzip
from news_puller.fetch import get_news
from news_puller.media import get_media
from news_puller.shares import update_twitter_counts, get_sharings
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
        'version': __version__,
        'startTime': start_time
    }
    return jsonify(response)


@app.route('/', methods=['GET'])
def index():
    news = Database.select_last_news(24)
    return jsonify(news)


@app.route('/fetch/<theme>', methods=['GET'])
def fetch_news(theme):
    news = get_news(theme)

    return jsonify(news)


@app.route('/get/<theme>/<int:since>', methods=['GET'])
@cross_origin()
def get_last_news(theme, since):
    news = Database.select_last_news(since, theme)

    return jsonify(news)


@app.route('/get/media/<theme>', methods=['GET'])
@cross_origin()
def fetch_media(theme):
    media = get_media(theme)

    return jsonify(media)


@app.route('/fetch/tweetCount/<int:since>', methods=['GET'])
def fetch_twitter_counts(since):
    counts = update_twitter_counts(since)

    return jsonify(counts)


@app.route('/get/tweets/<id>', methods=['GET'])
@cross_origin()
def get_tweets(id):
    tweets = get_sharings(id)

    return jsonify(tweets)
