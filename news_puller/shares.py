import news_puller.config as cfg
import tweepy
from news_puller.db import Database


auth = tweepy.OAuthHandler(cfg.TW_CONSUMER_KEY, cfg.TW_CONSUMER_SECRET)
auth.set_access_token(cfg.TW_ACCESS_TOKEN, cfg.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def tweepy_shares(new):
    tweet_list= []
    users = []
    
    try:
        tweets = tweepy.Cursor(api.search_tweets,
                               q='url:' + new['fullUrl'],
                               since_id=new.get('lastTweet', 0) + 1).items(100)
        print("Last tweet id: " new.get('lastTweet', 0))
        for tweet in tweets:
            twt = tweet._json
            print("Tweet id: " twt['id'])
            users.append({'_id': twt['user']['id'],
                          'name': twt['user']['name'],
                          'screen_name': twt['user']['screen_name'],
                          'image': twt['user']['profile_image_url_https']})

            tweet_list.append({'_id': twt['id'],
                               'created_at': twt['created_at'],
                               'text': twt['text'],
                               'new': new['_id'],
                               'user': twt['user']['id']})

        Database.save_tweets(tweet_list)
        Database.save_users(users)
        
    except Exception as e:
        logger.error('Something happened fetching tweets for: %s. %s', new['fullUrl'], e)

    return tweet_list
