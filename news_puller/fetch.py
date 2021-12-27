import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG
from news_puller.db import Database
from base64 import b64encode
import time


log = getLogger('werkzeug')
log.setLevel(DEBUG)


def select_image(new):
    if 'media_thumbnail' in new:
        return new['media_thumbnail'][0]['url']

    elif 'media_content' in new:
        return new['media_content'][0]['url']


def filter_feed(num_docs, theme, paper, news):
    filtered_news = []

    print('The paper ' + paper + ' has returned ' + str(len(news)) + ' news.')
    
    for item in news:
        try:
            if bool(item) :
                new = {'_id': b64encode(item['link']),
                       'url': item['link'],
                       'title': item['title'],
                       'paper': paper,
                       'theme': theme,
                       'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                       'topics' : [], # Database.calculate_idf(num_docs, item['title']),
                       'image': select_image(item)}

                filtered_news.append(new)

        except Exception as e:
            log.error('Something happened with new: ' + str(url))
            log.error(e)

    return filtered_news


def get_news(theme):
    total = []
    media = filter(lambda m: m['theme'] == theme, cfg.PAPER_LIST)
    
    print('Calcular el numero de noticias para el tema seleccionado')
    num_docs = Database.num_news(None, theme)
    
    for plist in media:
        print('Fetch ' + plist['paper'] + ' news from ' + plist['feed'])

        try:
            paper_news = feedparser.parse(plist['feed'])

            if paper_news.status == 200:
                news = filter_feed(num_docs, theme, plist['paper'], paper_news['entries'])
                Database.save_news(news)
                total += news

            else:
                log.error('Some connection error', paper_news.status)

        except Exception as e:
            log.error(e)
            log.error('Failed to load USE model, USE API won\'t be available')

    return total
