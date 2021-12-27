import news_puller.config as cfg
from logging import getLogger, DEBUG
from news_puller.db import Database
import requests
import re

    
log = getLogger('werkzeug')
log.setLevel(DEBUG)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {cfg.TW_BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2RecentTweetCountsNews"
    return r


def callTwitter(search_url, query_params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()


def getPath(url):
    m = re.search('https?:\/\/.+(\/.*)', url)
    return m.group(1)


def searchCount(new):
    path = getPath(new['url'])
    search_url = "https://api.twitter.com/2/tweets/counts/recent"
    query_params = {'query': 'url:' + path, 'granularity': 'day'}
    
    response = callTwitter(search_url, query_params)

    return response["meta"]["total_tweet_count"]


def get_sharings(id):
    tweet_list = []
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    new = Database.search_new(id)
    
    path = getPath(new['url'])
    query_params = {'query': 'url:' + path,
                    'max_results': 100,
                    'tweet.fields': 'created_at,public_metrics,text',
                    'user.fields': 'id,name,profile_image_url,username'}

    tweets = callTwitter(search_url, query_params)

    return tweets['data']


def update_twitter_counts(theme, period):
    news = Database.select_last_news(period, theme)

    for new in news:
        count = searchCount(new)
        if (new.get('tweetCount', 0) < count):
            Database.update(new._id, count)
