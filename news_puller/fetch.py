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


def select_image(new):
    if 'media_thumbnail' in new:
        return new['media_thumbnail'][0]['url']

    elif 'media_content' in new:
        return new['media_content'][0]['url']


def create_unique_id(url):
    message_bytes = url.encode()
    base64_bytes = b64encode(message_bytes)
    
    return base64_bytes.decode()


def getPath(url):
    m = re.findall(r'[^\/]+', url)
  
    return m[-1]

def filter_tags(theme, new):
  new_tags = []

  for t in new.get('tags',[]) : new_tags.append(t['term'].lower())

  if 'deportes' in new_tags:
    theme = 'deportes'
    new_tags.remove('deportes')

  if len(new_tags) < 2:
    for t in Database.select_topics(theme):
      if t['name'] in new['title'] + new.get('summary', ''):
        new_tags.append(t['name'])

  Database.save_topics(new_tags, theme)

  return theme, new_tags


def filter_feed(theme, paper, news):
  filtered_news = []
  print('The paper ' + paper + ' has returned ' + str(len(news)) + ' news.')
  
  for item in news:
    try:
      if bool(item) :
        link = item['link']
        id = create_unique_id(link)
        new = Database.search_new(id)
        if (new is None):
          theme, tags = filter_tags(theme, item)
          new = {'_id': id,
                 'fullUrl': link,
                 'name': getPath(link),
                 'title': item['title'],
                 'paper': paper,
                 'theme': theme,
                 'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                 'topics' : tags,
                 'image': select_image(item)}

          filtered_news.append(new)

        twitter_shares(new)

    except Exception as e:
        logger.error('Something happened with new: ' + item['link'])
        logger.error(e)

  return filtered_news


def get_news(paper):
    total = []
    media = filter(lambda m: m['paper'] == paper, cfg.PAPER_LIST)

    for plist in media:
        print('Fetch', plist['paper'], 'news from', plist['feed'])

        try:
            paper_news = feedparser.parse(plist['feed'])

            if paper_news.status == 200:
                news = filter_feed(plist['theme'], plist['paper'], paper_news['entries'])
                Database.save_news(news)
                total += news

            else:
                logger.error('Some connection error', paper_news.status)

        except Exception as e:
            logger.error(e)
            logger.error('Failed to load USE model, USE API won\'t be available')

    return total
