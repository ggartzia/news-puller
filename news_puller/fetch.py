import news_puller.config as cfg
import feedparser
from logging import getLogger, DEBUG
from news_puller.db import Database
from news_puller.shares import searchTweets
from base64 import b64encode
from math import log
import time


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

def split_title(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )

    s = s.lower()

    for a, b in replacements:
        s = s.replace(a, b)

    s = re.sub("[^a-zñç]", " ", s)

    return s.split()


def calculate_idf(num_docs, theme, title):
    topics = []
    
    try:
        idfs = {}
        
        for term in split_title(title):
            if term not in sw:
                # Use the number of docs that contain the term to calculate the IDF
                term_docs = Database.num_news({'theme': theme, 'title' : {'$regex' : term}})
                idfs[term] = log((num_docs - term_docs + 0.5) / (term_docs + 0.5))

        idfs = {k: v for k, v in idfs.items() if v > cfg.TF_IDF_MIN_WEIGHT}
        
        topics = list(idfs.keys())
    
    except Exception as e:
        logger.error(e)
        
    return topics[:4]


def filter_feed(num_docs, theme, paper, news):
    filtered_news = []

    print('The paper ' + paper + ' has returned ' + str(len(news)) + ' news.')
    
    for item in news:
        try:
            if bool(item) :
                link = item['link']
                name = getPath(link)
                title = item['title']
                new = {'_id': create_unique_id(link),
                       'fullUrl': link,
                       'name': name,
                       'title': title,
                       'paper': paper,
                       'theme': theme,
                       'published': time.strftime("%Y-%m-%d %H:%M:%S", item['published_parsed']),
                       'topics' : Database.calculate_idf(num_docs, theme, title),
                       'tweetCount' : searchTweets(name),
                       'image': select_image(item)}

                filtered_news.append(new)

        except Exception as e:
            logger.error('Something happened with new: ' + item['link'])
            logger.error(e)

    return filtered_news


def get_news(paper):
    total = []
    media = filter(lambda m: m['paper'] == paper, cfg.PAPER_LIST)
    
    print('Numero de periodicos:', media)

    print('Calcular el numero de noticias para el tema seleccionado')
    num_docs = Database.num_news({})
    
    print('Numero de noticias:', num_docs)

    for plist in media:
        print('Fetch', plist['paper'], 'news from', plist['feed'])

        try:
            paper_news = feedparser.parse(plist['feed'])

            if paper_news.status == 200:
                news = filter_feed(num_docs, plist['theme'], plist['paper'], paper_news['entries'])
                Database.save_news(news)
                total += news

            else:
                logger.error('Some connection error', paper_news.status)

        except Exception as e:
            logger.error(e)
            logger.error('Failed to load USE model, USE API won\'t be available')

    return total
