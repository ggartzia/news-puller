import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG
from news_puller.db import Database
from news_puller.shares import tweepy_shares
from base64 import b64encode
import html
import time
import os
import re


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

NUM_NEWS_PARSE = 50

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, 'spanish.txt')
STOP_WORDS = []

with open(STOP_WORDS_DIR, 'rb') as language_file:
    STOP_WORDS = [line.decode('utf-8').strip()
                  for line in language_file.readlines()]


def select_image(new):
    thumb_image = ''

    if 'media_thumbnail' in new:
        thumb_image = new['media_thumbnail'][0]['url']
    
    elif 'media_content' in new:
        thumb_image = new['media_content'][0]['url']
 
    elif 'enclosure' in new:
        thumb_image = new['enclosure'][0]['url']

    elif 'links' in new:
        images = list(filter(lambda l: l['rel'] == 'enclosure', new['links']))
        thumb_image = images[0]['href']

    return thumb_image


def clean_html(text):
    html_decoded_string = html.unescape(text)
    return re.sub(r'<(.|\n)*?>', '', html_decoded_string)


def get_description(new):
    description = ''

    if 'dc_abstract' in new:
        description = new['dc_abstract']
        
    elif 'summary' in new:
        description = new['summary']

    elif 'description' in new:
      description = new['description']
    
    elif 'media_description' in new:
      description = new['media_description']
    
    # Remove html tags from description
    return clean_html(description)


def create_unique_id(url):
    message_bytes = url.encode()
    base64_bytes = b64encode(message_bytes)
    
    return base64_bytes.decode()


def split_tags(text):
    #remove punctuation and split into seperate words
    text = re.findall(r'[a-záéíóúñç]+', text.lower(), flags = re.UNICODE)
    
    words = list(filter(lambda x: x not in STOP_WORDS and len(x) > 2, text))
    
    double_tags = list(zip(*[words[i:] for i in range(2)]))

    return list(map(lambda l: ' '.join(l), double_tags))


def get_tags(title, description, theme):
    tags = split_tags(title) + split_tags(description)
    tags = Database.save_topics(tags, theme)

    return tags


def filter_feed(theme, paper, news):
    twitter_exceded = False
    # Parse only a given number of news to avoid TimeOut Exception
    for item in news[:NUM_NEWS_PARSE]:
        try:
            if bool(item) :
                link = item['link']
                id = create_unique_id(link)
                new = Database.search_new(id)

                if (new is None):
                    title = clean_html(item['title'])
                    description = get_description(item)
                    new = {'id': id,
                           'fullUrl': link,
                           'title': title,
                           'description': description,
                           'paper': paper,
                           'theme': theme,
                           'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                           'topics': get_tags(title, description, theme),
                           'tweetCount': 0
                          }

                if not twitter_exceded:
                    tweet_list = tweepy_shares(new)

                    if (tweet_list == -1):
                        twitter_exceded = True
                    elif (len(tweet_list) > 0):
                        print("BEFORE ORDERING:", tweet_list[0]['_id'], tweet_list[-1]['_id'])
                        tweet_list = sorted(tweet_list, key=lambda t: t['_id'])
                        print("AFTER ORDERING:", tweet_list[0]['_id'], tweet_list[-1]['_id'])
                        new['lastTweet'] = tweet_list[0]['_id']
                        print("iNCREASE TWEETS", new['tweetCount'], len(tweet_list))
                        new['tweetCount'] += len(tweet_list)
                        print("uPDATED", new['tweetCount'])

                new['image'] = select_image(item)

                Database.save_new(new)

        except Exception as e:
            logger.error('Something happened with new: %s. %s', item['link'], e)

    pass


def get_news(paper):
    try:
        media = cfg.PAPER_LIST[paper]
        paper_news = feedparser.parse(media['feed'])

        if paper_news.status == 200:
            filter_feed(media['theme'], media['paper'], paper_news['entries'])
        else:
            logger.error('Some connection error', paper_news.status)

    except Exception as e:
        logger.error('Failed to load USE model, USE API won\'t be available: %s', e)

    pass
