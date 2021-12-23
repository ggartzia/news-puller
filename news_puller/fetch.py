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


def filter_feed(num_docs, theme, paper, news):
    filtered_news = []

    print('The paper ' + paper + ' has returned ' + str(len(news)) + ' news.')
    
    for item in news:
        try:
            if bool(item) :
                title = item['title']
                new = {'_id': item['link'],
                       'title': title,
                       'paper': paper,
                       'theme': theme,
                       'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                       'topics' : Database.calculate_idf(num_docs, title),
                       'image': select_image(item)}

                filtered_news.append(new)

        except:
            log.error('Something happened with new: ' + str(item))

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

        except:
            log.error('Failed to load USE model, USE API won\'t be available')

    return total
