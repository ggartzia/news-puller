import requests
import hashlib
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from news_puller.db.new import search_new, save_new
from news_puller.db.media import search_media
from news_puller.db.topic import save_topics
from news_puller.tfidf import TfIdfAnalizer


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
                    media = search_media(tweet['user']['screen_name'])

                    soup = BeautifulSoup(page.text, 'html.parser')
                    text = self.extract_text(media['text_container'], soup)
                    title = self.extract_title(soup)
                    description = self.extract_description(soup)

                    topics = self.TFIDF.get_topics(title, description, text)

                    new = {'_id': new_id,
                           'fullUrl': url,
                           'title': title,
                           'description': description,
                           'paper': media['_id'],
                           'theme': media['theme'],
                           'published': self.extract_date(soup),
                           'topics': topics,
                           'image': self.extract_image(soup),
                           'retweet_count': tweet['retweet_count'],
                           'favorite_count': tweet['favorite_count'],
                           'reply_count': tweet['reply_count']
                          }
                    
                    save_topics(topics, media['theme'])
                    save_new(new)

                    return new_id

            except Exception as e:
                logging.error('There was an error parsing new url: %s. %s', url, e)

        else:
            return new_id

        return None


    def create_unique_id(self, url): 
        return hashlib.sha256(url.encode('utf-8')).hexdigest()


    def extract_description(self, body):
        description = ''

        tag = body.find("meta", property="og:description")
        if tag is not None:
            description = tag['content']

        return description


    def extract_title(self, body):
        title = ''

        if body.find("meta", property="og:title") is not None:
            title = body.find("meta", property="og:title")['content']

        elif body.find("title") is not None:
            title = body.find("title")
        
        return title


    def extract_text(self, container_class, body):
        article = None
        text = []

        try:
            if container_class is not None and body.find("div", {"class": container_class}) is not None:
                article = body.find("div", {"class": container_class})

            if article is None and body.find("article") is not None:
                article = body.find("article")

            if article is not None:
                text = [e.get_text().lower() for e in article.find_all('p')]

        except Exception as e:
            logging.error('There is no text on article: %s. %s', body.find("title"), e)

        return text


    def extract_date(self, body):
        date = ''

        if body.find("meta", property="article:published_time") is not None:
            date = body.find("meta", property="article:published_time")['content']

        elif body.find("meta", property="article:modified_time") is not None:
            date = body.find("meta", property="article:modified_time")['content']

        elif body.find("meta", property="og:updated_time") is not None:
            date = body.find("meta", property="og:updated_time")['content']

        else:
            date = datetime.now()
            date = date.strftime("%Y-%m-%dT%H:%M:%S%z")

        return date


    def extract_image(self, body):
        image = ''

        if body.find("meta", property="twitter:image") is not None:
            image = body.find("meta", property="twitter:image")

        elif body.find("meta", property="og:image") is not None:
            image = body.find("meta", property="og:image")

        elif body.find("meta", {"data-ue-u": "twitter:image"}) is not None:
            image = body.find("meta", {"data-ue-u": "twitter:image"})

        elif body.find("meta", {"data-ue-u": "og:image"}) is not None:
            image = body.find("meta", {"data-ue-u": "og:image"})

        if image is not None:
            return image['content']

