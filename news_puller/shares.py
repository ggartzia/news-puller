import news_puller.config as cfg
import tweepy
import json
from logging import getLogger, DEBUG
from news_puller.db import Database

log = getLogger('werkzeug')
log.setLevel(DEBUG)

# 4 cadenas para la autenticacion
auth = tweepy.OAuthHandler(cfg.TW_CONSUMER_KEY, cfg.TW_CONSUMER_SECRET)
auth.set_access_token(cfg.TW_ACCESS_TOKEN, cfg.TW_ACCESS_TOKEN_SECRET)

# con este objeto realizaremos todas las llamadas al API
api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def search(url):
    log.debug('Search this URL in Twitter: ' + url)
    query = "url:" + url
    tweet_list = tweepy.Cursor(api.search, q=query)
    for tweet in tweet_list.items(1):
        print(json.dumps(tweet._json, indent=4))

    return tweet_list


def get_sharings():
    tweets = []
    news = Database.select_last_news(24)

    for item in news:
        tweets.append(search(item['_id']))

    Database.save('tweets', tweets)
    return tweets

