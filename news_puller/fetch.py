import feedparser
from logging import getLogger, DEBUG
from news_puller.db.new import search_new, save_new
from news_puller.db.media import search_media
from news_puller.db.topic import save_topics
from news_puller.shares import tweepy_shares
from news_puller.tfidf import get_topics
from base64 import b64encode
import html
import time
import re


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

NUM_NEWS_PARSE = 50


def select_image(new):
    thumb_image = ''

    try:  
        if 'media_thumbnail' in new:
            thumb_image = new['media_thumbnail'][0]['url']
        
        elif 'media_content' in new:
            thumb_image = new['media_content'][0]['url']
     
        elif 'enclosure' in new:
            thumb_image = new['enclosure'][0]['url']

        elif 'links' in new:
            images = list(filter(lambda l: l['rel'] == 'enclosure', new['links']))
            thumb_image = images[0]['href']

    except Exception as e:
        logger.error('Failed getting an image for article %s. Error: %s', new['link'], e)

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


def filter_feed(theme, paper, news):
    twitter_exceded = False

    # Parse only a given number of news to avoid TimeOut Exception
    for item in news[:NUM_NEWS_PARSE]:
        try:
            if bool(item) :
                link = item['link']
                id = create_unique_id(link)
                new = search_new(id)

                if new is None:
                    title = clean_html(item['title'])
                    description = get_description(item)
                    new = {'id': id,
                           'fullUrl': link,
                           'title': title,
                           'description': description,
                           'paper': paper,
                           'theme': theme,
                           'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                           'topics': get_topics([title + ' ' + description]),
                           'tweetCount': 0
                          }

                if not twitter_exceded:
                    tweet_list = tweepy_shares(new)

                    if (tweet_list == -1):
                        twitter_exceded = True
                    elif (len(tweet_list) > 0):
                        new['lastTweet'] = tweet_list[0]['_id']
                        new['tweetCount'] += len(tweet_list)

                new['image'] = select_image(item)

                save_new(new)

        except Exception as e:
            logger.error('Something happened with new: %s. %s', item['link'], e)

    pass


def get_news(paper):
    try:
        media = search_media(paper)
        paper_news = feedparser.parse(media['feed'])

        if paper_news.status == 200:
            filter_feed(media['theme'], media['paper'], paper_news['entries'])
        else:
            logger.error('Some connection error', paper_news.status)

    except Exception as e:
        logger.error('Failed to load USE model, USE API won\'t be available: %s', e)

    pass
