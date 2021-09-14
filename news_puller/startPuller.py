from news_puller.fetch import get_news
from news_puller.save import save
from . import __version__
from time import time
from logging import getLogger, ERROR
from flask import Flask, jsonify
from flask_gzip import Gzip

start_time = int(time())
log = getLogger('werkzeug')
log.setLevel(ERROR)

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


@app.route('/fetch/news', methods=['GET'])
def use_embeddings():
    news = get_news()
    save(news)

    return jsonify(news)


