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
STOP_WORDS = load_file()


def load_file():
    stop_words = []
    with open('spanish.txt', 'rb') as language_file:
        stop_words = [line.decode('utf-8').strip()
                      for line in language_file.readlines()]
    
    return stop_words

    
def select_image(new):
    if 'media_thumbnail' in new:
        return new['media_thumbnail'][0]['url']
    
    elif 'media_content' in new:
        return new['media_content'][0]['url']
    
    print('Enclosure image', new['enclosure'])
    return new['enclosure']


def get_description(new):
    if 'media_description' in new:
        print('Descripcion limpia', new['media_description'])
        return new['media_description']
    
    elif 'dc_abstract' in new:
        return new['dc_abstract']
    
    elif 'summary' in new:
        return new['summary']
    
    # clean description of html tags
    return new['description']


def create_unique_id(url):
    message_bytes = url.encode()
    base64_bytes = b64encode(message_bytes)
    
    return base64_bytes.decode()


def get_path(url):
    m = re.findall(r'[^\/]+', url)
  
    return m[-1]


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s.title()


def filter_tags(theme, new):
    new_tags = []
  
    text = new['title'] + ' ' + new.get('description', '')

    #remove punctuation and split into seperate words
    words = re.findall(r'\w+', text.lower(), flags = re.UNICODE | re.LOCALE)
    
    new_tags = filter(lambda x: x not in STOP_WORDS, words)
    print("Removed stop words with our STOP_WORDS", new_tags)
    
    new_tags = new_tags + zip(*[new_tags[i:] for i in range(2)])
    
    # We have to check the usage of the words in the database
    new['topics'] = new_tags
    Database.save_topics(new_tags, theme)

    return new


def filter_feed(theme, paper, news):
  filtered_news = []
  
  for item in news:
    try:
      if bool(item) :
        link = item['link']
        id = create_unique_id(link)
        new = Database.search_new(id)

        if (new is None):
          new = {'_id': id,
                 'fullUrl': link,
                 'name': get_path(link),
                 'title': item['title'],
                 'description': get_description(item),
                 'paper': paper,
                 'theme': theme,
                 #pubDate OR updated
                 'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed'])
                }
            new = filter_tags(theme, new)

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
