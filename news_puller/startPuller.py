from time import time
from flask import Flask, jsonify
from flask_gzip import Gzip
from news_puller.fetch import get_news
from news_puller.media import get_media
from news_puller.db import Database
import news_puller.scheduler


start_time = int(time())

app = Flask(__name__)
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
def get_last_news(theme, since):
    news = Database.select_last_news(since, theme)

    return jsonify(news)


@app.route('/get/media/<theme>', methods=['GET'])
def fetch_media(theme):
    media = get_media(theme)

    return jsonify(media)
