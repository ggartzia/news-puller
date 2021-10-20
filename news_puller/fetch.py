import numpy as np
import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG

log = getLogger('werkzeug')
log.setLevel(DEBUG)

feed_fields = ['title', 'link', 'published', 'tags', 'media_thumbnail', 'media_content']


def filter_feed(paper, news):
    log.debug(news)
    for idx, item in enumerate(news):
        news[idx] = {k: v for k, v in item.items() if k in feed_fields}.update({'paper', paper})

    return news


def get_news():
    news = []

    for plist in cfg.paper_list:
        log.debug('Fetch ' + plist['paper'] + ' news from ' + plist['feed'])

        try:
            paper_news = feedparser.parse(plist['feed'])
            log.debug(paper_news)
            if paper_news.status == 200:
                news = news + filter_feed(plist['paper'], paper_news['entries'])

            else:
                log.warning("Some connection error", paper_news.status)

        except:
            log.error('Failed to load USE model, USE API won\'t be available')

    return np.array(news).tolist()
