import news_puller.config as cfg
from news_puller.db import Database
import requests
import tweepy
import json


auth = tweepy.OAuthHandler(cfg.TW_CONSUMER_KEY, cfg.TW_CONSUMER_SECRET)
auth.set_access_token(cfg.TW_ACCESS_TOKEN, cfg.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {cfg.TW_BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2RecentTweetCountsNews"
    return r


def searchTweets(url):
    count = 0

    try:
        tweets = tweepy.Cursor(api.search_tweets, q='url:' + url, count=1000).items()

        count = sum(1 for _ in tweets)

    except Exception as e:
        print(e)

    return count


def callTwitter(search_url, query_params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()


def get_sharings(id):
    tweet_list = []
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    new = Database.search_new(id)

    query_params = {'query': 'url:' + new['name'],
                    'max_results': 100,
                    'tweet.fields': 'created_at,public_metrics,text',
                    'user.fields': 'id,name,profile_image_url,username'}

    tweets = callTwitter(search_url, query_params)

    return tweets['data']


def update_twitter_counts(theme, period):
    news = Database.select_last_news(period, theme)

    for new in news:
        count = searchTweets(new['name'])
        if (new.get('tweetCount', 0) < count):
            Database.update(new['_id'], count)
