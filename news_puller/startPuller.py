from news_puller.fetch import get_news
from . import __version__
from time import time
from logging import getLogger, DEBUG
from flask import Flask, jsonify, redirect
from flask_gzip import Gzip

start_time = int(time())
log = getLogger('werkzeug')
log.setLevel(DEBUG)

app = Flask(__name__)
Gzip(app)


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
    return redirect('fetch/news')


@app.route('/fetch/news', methods=['GET'])
def use_embeddings():
    news = get_news()

    return jsonify(news)


