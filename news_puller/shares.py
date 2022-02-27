import news_puller.config as cfg
import requests
import tweepy
import json


auth = tweepy.OAuthHandler(cfg.TW_CONSUMER_KEY, cfg.TW_CONSUMER_SECRET)
auth.set_access_token(cfg.TW_ACCESS_TOKEN, cfg.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {cfg.TW_BEARER_TOKEN}"
    r.headers["User-Agent"] = 'v2RecentTweetCountsNews'
    return r


def callTwitter(search_url, query_params):
    response = requests.request('GET', search_url, auth=bearer_oauth, params=query_params)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    return response.json()


def tweepy_shares(new):
    tweet_list= []
    users = []
    query_params = {'query': 'url:' + new['fullUrl'],
                    'expansions': 'author_id',
                    'tweet.fields': 'id,created_at,author_id,text',
                    'user.fields': 'id,name,profile_image_url,username'}

    for tweet in tweepy.Cursor(api.search_tweets,
                               q='url:' + new['fullUrl'],
                               since_id=int(new.get('lastTweet', 0)) + 1).items(100):
        print(tweet._json)


    if 'data' in tweets:
        print('this is the data recieved:', data)
        tweet_list = [dict(twt, **{'new':new['_id'], '_id': twt['id']}) for twt in tweets['data']]
        new['lastTweet'] = tweets['meta']['newest_id']
        new['tweetCount'] = new.get('tweetCount', 0) + len(tweet_list)
        
    if 'includes' in tweets:
        users = [dict(user, **{'_id': user['id']}) for user in tweets['includes']['users']]

    return new, tweet_list, users


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
        print('this is the data recieved:', data)
        tweet_list = [dict(twt, **{'new':new['_id'], '_id': twt['id']}) for twt in tweets['data']]
        new['lastTweet'] = tweets['meta']['newest_id']
        new['tweetCount'] = new.get('tweetCount', 0) + len(tweet_list)
        
    if 'includes' in tweets:
        users = [dict(user, **{'_id': user['id']}) for user in tweets['includes']['users']]

    return new, tweet_list, users
