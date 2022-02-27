import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG
from news_puller.db import Database
from news_puller.shares import twitter_shares
from base64 import b64encode
import time
import re


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


CLEANR = re.compile('<.*?>')
STOP_WORDS = []
with open('./spanish.txt', 'rb') as language_file:
    STOP_WORDS = [line.decode('utf-8').strip()
                  for line in language_file.readlines()]


def select_image(new):
    if 'media_thumbnail' in new:
        return new['media_thumbnail'][0]['url']
    
    elif 'media_content' in new:
        return new['media_content'][0]['url']
    
    print('Enclosure image', new['enclosure'])
    return new['enclosure']


def get_description(new):
    description = ''

    if 'media_description' in new:
        description = re.sub(CLEANR, '', new['media_description'])
    
    elif 'dc_abstract' in new:
        description = new['dc_abstract']
    
    elif 'summary' in new:
        description = new['summary']

    else:
      description = new['description']

    return description


def create_unique_id(url):
    message_bytes = url.encode()
    base64_bytes = b64encode(message_bytes)
    
    return base64_bytes.decode()


def get_path(url):
    m = re.findall(r'[^\/]+', url)
  
    return m[-1]


def split_tags(text):
    #remove punctuation and split into seperate words
    text = re.findall(r'\w+', text.lower(), flags = re.UNICODE | re.LOCALE)
    
    new_tags = filter(lambda x: x not in STOP_WORDS, words)
    print("Removed stop words with our STOP_WORDS", new_tags)
    
    new_tags = new_tags + zip(*[new_tags[i:] for i in range(2)])

    return new_tags


def get_tags (title, description):
    tags = split_tags(title) + split_tags(description)

    print("Calculated tags", tags)
    tags = list(dict.fromkeys(tags))

    Database.save_topics(tags)

    return tags


def filter_feed(theme, paper, news):
  filtered_news = []
  
  for item in news:
    try:
      if bool(item) :
        link = item['link']
        id = create_unique_id(link)
        new = Database.search_new(id)

        if (new is None):
            title = item['title']
            description = get_description(item)
            new = {'_id': id,
                   'fullUrl': link,
                   'name': get_path(link),
                   'title': title,
                   'description': description,
                   'paper': paper,
                   'theme': theme,
                   #pubDate OR updated
                   'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                   'topics': get_tags(title, description)
                  }

            Database.save_topics(new['topics'])

        new, tweets, users = twitter_shares(new)
        Database.save_tweets(tweets)
        Database.save_users(users)

        new['image'] = select_image(item)
        
        filtered_news.append(new)

    except Exception as e:
        logger.error('Something happened with new: %s. %s', item['link'], e)

  return filtered_news


def get_news(paper):
    total = []
    media = filter(lambda m: m['paper'] == paper, cfg.PAPER_LIST)

    for plist in media:
        try:
            paper_news = feedparser.parse(plist['feed'])

            if paper_news.status == 200:
                news = filter_feed(plist['theme'], plist['paper'], paper_news['entries'])
                Database.save_news(news)
                total += news

            else:
                logger.error('Some connection error', paper_news.status)

        except Exception as e:
            logger.error('Failed to load USE model, USE API won\'t be available: %s', e)

    return total
