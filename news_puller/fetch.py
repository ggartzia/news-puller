import numpy as np
import news_puller.config as cfg
import feedparser
import logging


feed_fields = ['title', 'link', 'published', 'tags', 'media_thumbnail', 'media_content']

def filter_feed(paper, news):
  for idx, item in enumerate(news):
    news[idx] = {k: v for k, v in item.items() if k in feed_fields}.update({'paper', paper})
  
  return news

def get_news():
    news = []

    try:
      for plist in cfg.paper_list:
        logging.debug('Fetch news from ' + plist['paper'])

        paper_news = feedparser.parse(plist['feed'])
        paper_news = filter_feed(plist['paper'], paper_news.entries)
        news = news + paper_news

    except:
      logging.warning('Failed to load USE model, USE API won\'t be available')

    return np.array(news).tolist()
