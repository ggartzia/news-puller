import news_puller.config as cfg
import requests
import json


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {cfg.TW_BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2RecentTweetCountsNews"
    return r


def callTwitter(search_url, query_params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()


def shareCount(name):
    count = 0

    if name:
        search_url = "https://api.twitter.com/2/tweets/counts/recent"
        query_params = {'query': 'url:' + name, 'granularity': 'day'}

        response = callTwitter(search_url, query_params)
        count = response["meta"]["total_tweet_count"]

    return count


def twitter_shares(new):
    tweet_list= []
    
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': 'url:' + new['name'],
                    'max_results': 100,
                    'tweet.fields': 'id,created_at,author_id, text',
                    'expansions': 'author_id',
                    'user.fields': 'id,name,profile_image_url,username'}

    if "last_tweet" in new:
        query_params['since_id'] = new['last_tweet']

    try:
      tweets = callTwitter(search_url, query_params)
      tweet_list = [dict(twt, **{'new':new['_id'], '_id': twt['id']}) for twt in tweets['data']]
      new['last_tweet'] = tweets['meta']['newest_id']
        
    except Exception as e:
      print(e)
        
    return new, tweet_list
