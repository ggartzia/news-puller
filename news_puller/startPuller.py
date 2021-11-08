from . import __version__
from time import time
from flask import Flask, jsonify, redirect, render_template
from flask_gzip import Gzip
from news_puller.fetch import get_news
from news_puller.db import Database
from news_puller.shares import get_sharings
from news_puller.fake_news import fact_check

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


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')


@app.route('/fetch/news', methods=['GET'])
def fetch_news():
    news = get_news()

    return jsonify(news)


@app.route('/fetch/fake_news', methods=['GET'])
def fetch_fakes():
    fakes = fact_check()

    return jsonify(fakes)


@app.route('/fetch/shares', methods=['GET'])
def fetch_shares():
    sharings = get_sharings()

    return jsonify(sharings)


@app.route('/get/news', methods=['GET'])
def get_last_news():
    news = Database.select_last_news(24)

    return jsonify(news)

