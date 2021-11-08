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


def searchTweets(url, since_id):
    tweet_list = []

    #  + ' -is:retweet&max_results=100&tweet.fields=user,created_at,text,id,user,retweeted_status,retweet_count,favorite_count'
    query = 'url:' + url

    tweets = tweepy.Cursor(api.search,
                           q=query,
                           result_type='recent',
                           since_id=since_id).items(1500)

    for tw in tweets:
        tweet = {}
        tweet['new'] = url
        tweet['_id'] = tw.id
        tweet['date'] = tw.created_at
        tweet['user'] = tw.user.screen_name
        tweet['text'] = tw.text
        tweet_list.append(tweet)

    return tweet_list


def get_sharings():
    news = Database.select_last_news(1)

    for item in news:
        url = item['_id']
        since_id = Database.latest_tweet_id(url)
        log.debug('Search this URL in Twitter: ' + url + ' from id ' + str(since_id))
        tweets = searchTweets(url, since_id)
        if tweets:
            Database.save('tweets', tweets)

