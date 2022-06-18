import requests
import hashlib
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from news_puller.db.new import search_new, save_new
from news_puller.db.media import search_media
from news_puller.db.topic import save_topics
from news_puller.tfidf import TfIdfAnalizer
import sys


class NewsScrapper(object):

    def __init__(self):
        self.TFIDF = TfIdfAnalizer()


    def scrap(self, tweet, url):
        new_id = self.create_unique_id(url)

        if search_new(new_id) is None:

            try:
                page = requests.get('https://news-puller.herokuapp.com/')
                page = requests.get(url)
                if (page.status_code == 200):
                    soup = BeautifulSoup(page.text, 'html.parser')

                    text = self.get_text(soup)
                    
                    if len(text) > 0:
                        topics = self.TFIDF.get_topics(text)

                        media = search_media(tweet['user']['screen_name'])

                        new = {'_id': new_id,
                               'fullUrl': url,
                               'title': self.get_title(soup),
                               'description': self.get_description(soup),
                               'paper': media['_id'],
                               'theme': media['theme'],
                               'published': self.get_date(soup),
                               'topics': topics,
                               'image': self.get_image(soup),
                               'retweet_count': tweet['retweet_count'],
                               'favorite_count': tweet['favorite_count'],
                               'reply_count': tweet['reply_count']
                              }
                        
                        save_topics(topics, media['theme'])
                        save_new(new)

                        return new_id
                    else:
                        logging.warning("THE CONTENT OF THE URL IS EMPTY!! %s", url)

            except Exception as e:
                logging.error('There was an error parsing new url: %s. %s', url, e)

        else:
            return new_id

        return None


    def create_unique_id(self, url): 
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def get_description(self, body):
        description = ''

        tag = body.find("meta", property="og:description")
        if tag is not None:
            description = tag['content']
        
        # Remove html tags from description
        return description


    def get_title(self, body):
        title = ''

        tag = body.find("meta", property="og:title")
        if body.find("meta", property="og:title") is not None:
            title = body.find("meta", property="og:title")['content']
        elif body.find("title") is not None:
            title = body.find("title")
        
        return title


    def get_text(self, body):
        article = None
        text = []

        if body.find("div", {"class": "article-text"}) is not None:
            article = body.find("div", {"class": "article-text"})
        elif body.find("div", {"class": "card-body-article"}) is not None:
            article = body.find("div", {"class": "card-body-article"})
        elif body.find("div", {"class": "content-container"}) is not None:
            article = body.find("div", {"class": "content-container"})
        elif body.find("div", {"class": "article-modules"}) is not None:
            article = body.find("div", {"class": "article-modules"})
        elif body.find("div", {"class": "article-body-content"}) is not None:
            article = body.find("div", {"class": "article-body-content"})
        elif body.find("div", {"data-dtm-region": "articulo_cuerpo"}) is not None:
            article = body.find("div", {"data-dtm-region": "articulo_cuerpo"})
        elif body.find("div", {"class": "ue-c-article__body"}) is not None:
            article = body.find("div", {"class": "ue-c-article__body"})

        elif body.find("article") is not None:
            article = body.find("article")
        
        if article is not None:
            text = [e.get_text().lower() for e in article.find_all('p')]

        return text


    def get_date(self, body):
        date = ''

        tag = body.find("meta", property="article:published_time")
        if body.find("meta", property="article:published_time") is not None:
            date = body.find("meta", property="article:published_time")['content']

        elif body.find("meta", property="article:modified_time") is not None:
            date = body.find("meta", property="article:modified_time")['content']

        elif body.find("meta", property="og:updated_time") is not None:
            date = body.find("meta", property="og:updated_time")['content']

        else:
            date = datetime.now()
            date = date.strftime("%Y-%m-%dT%H:%M:%S%z")

        # Remove html tags from description
        return date


    def get_image(self, body):
        image = ''

        if body.find("meta", property="twitter:image") is not None:
            image = body.find("meta", property="twitter:image")['content']
        elif body.find("meta", property="og:image") is not None:
            image = body.find("meta", property="og:image")['content']
        elif body.find("meta", {"data-ue-u": "twitter:image"}) is not None:
            image = body.find("meta", {"data-ue-u": "twitter:image"})['content']
        elif body.find("meta", {"data-ue-u": "og:image"}) is not None:
            image = body.find("meta", {"data-ue-u": "og:image"})['content']
        
        # Remove html tags from description
        return image