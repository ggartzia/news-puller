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

  for t in new.get('tags',[]) : new_tags.append(normalize(t['term']))
  # remove duplicates from list
  new_tags = list(dict.fromkeys(new_tags))
    
  if len(new_tags) < 3:
    text = normalize(new['title'] + ' ' + new.get('summary', ''))
    possible_topics = Database.select_topics(theme, 100)

    while len(new_tags) < 4 and len(possible_topics) > 0:
      topic_name = possible_topics.pop(0)['name']

      if topic_name not in new_tags and topic_name in text:
        new_tags.append(topic_name)

  Database.save_topics(new_tags, theme)

  return new_tags


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
                 'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                 'topics' : filter_tags(theme, item)}

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
