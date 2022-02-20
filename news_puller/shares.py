import news_puller.config as cfg
import requests
import json


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {cfg.TW_BEARER_TOKEN}"
    r.headers["User-Agent"] = 'v2RecentTweetCountsNews'
    return r


def callTwitter(search_url, query_params):
    response = requests.request('GET', search_url, auth=bearer_oauth, params=query_params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()


def twitter_shares(new):
    tweet_list= []
    users = []
    
    search_url = 'https://api.twitter.com/2/tweets/search/all'
    query_params = {'query': 'url:' + new['fullUrl'],
                    'max_results': 100,
                    'expansions': 'author_id',
                    'tweet.fields': 'id,created_at,author_id,text',
                    'user.fields': 'id,name,profile_image_url,username'}

    if 'lastTweet' in new:
        query_params['since_id'] = int(new['lastTweet']) + 1

    tweets = callTwitter(search_url, query_params)
    
    if 'data' in tweets:
      tweet_list = [dict(twt, **{'new':new['_id'], '_id': twt['id']}) for twt in tweets['data']]
      new['lastTweet'] = tweets['meta']['newest_id']
      new['tweetCount'] = new.get('tweetCount', 0) + len(tweet_list)
        
    if 'includes' in tweets:
        users = [dict(user, **{'_id': user['id']}) for user in tweets['includes']['users']]

    return new, tweet_list, users
