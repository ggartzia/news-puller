import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG
from news_puller.db import Database
import time

log = getLogger('werkzeug')
log.setLevel(DEBUG)


def filter_tags(tags):
    new_tags = []

    for t in tags : new_tags.append(t['term'])
    return new_tags


def select_image(new):
    if 'media_thumbnail' in new:
        return new['media_thumbnail'][0]['url']

    elif 'media_content' in new:
        return new['media_content'][0]['url']



def filter_feed(paper, news):
    filtered_news = []

    log.debug('The paper ' + paper + ' has returned ' + str(len(news)) + ' news.')

    for item in news:
        try:
            new = {}
            new['_id'] = item['link']
            new['title'] = item['title']
            new['paper'] = paper
            new['published'] = time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed'])
            new['image'] = select_image(item)

            if 'tags' in item:
                new['tags'] = filter_tags(item['tags'])

            filtered_news.append(new)

        except:
            log.error('Something happened with new: ' + str(item))

    return filtered_news


def get_news():
    news = []

    for plist in cfg.PAPER_LIST:
        log.debug('Fetch ' + plist['paper'] + ' news from ' + plist['feed'])

        try:
            paper_news = feedparser.parse(plist['feed'])

            if paper_news.status == 200:                
                news += filter_feed(plist['paper'], paper_news['entries'])

            else:
                log.warning('Some connection error', paper_news.status)

        except:
            log.error('Failed to load USE model, USE API won\'t be available')

    Database.save('news', news)

    return news
