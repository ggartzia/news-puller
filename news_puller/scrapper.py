import requests
from bs4 import BeautifulSoup
from logging import getLogger, DEBUG
from news_puller.db.new import search_new, save_new
from news_puller.db.media import search_media
from news_puller.db.topic import save_topics
from news_puller.tfidf import TfIdfAnalizer
import news_puller.utils as utils


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class NewsScrapper(object):

    def __init__(self):
        self.TFIDF = TfIdfAnalizer()


    def scrap(self, url, paper):
        new_id = utils.create_unique_id(url)
        title = ''
        desc = ''
        date = ''
        topics = []
        image = ''

        if search_new(new_id) is None:

            try:
                page = requests.get(url)
                if (page.status_code == 200):
                    soup = BeautifulSoup(page.text, 'html.parser')

                    title = self.get_title(soup)
                    desc = self.get_description(soup)
                    date = self.get_date(soup)
                    image =  self.get_image(soup)

                    text = self.get_text(soup)
                    topics = self.TFIDF.get_topics(text)

                    media = search_media(paper)

                    new = {'id': new_id,
                           'fullUrl': url,
                           'title': self.get_title(soup),
                           'description': self.get_description(soup),
                           'paper': media['_id'],
                           'theme': media['theme'],
                           'published': self.get_date(soup),
                           'topics': topics,
                           'image': self.get_image(soup)
                          }
                    
                    save_topics(topics, media['theme'])
                    save_new(new)

                    return new_id

            except Exception as e:
                logger.error('There was an error parsing new url: %s, title: %s, description: %s, date: %s, image: %s, topics: %s. %s', url, title, desc, date, image, topics, e)

        else:
            return new_id

        return None


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

        if body.find("article") is not None:
            article = body.find("article")
        elif body.find("div", {"class": "article-text"}) is not None:
            article = body.find("div", {"class": "article-text"})
        
        text = [e.get_text() for e in article.find_all('p')]
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
        
        print("time!!!!!! %s", date)
        # Remove html tags from description
        return utils.parse_date(date)


    def get_image(self, body):
        image = ''

        tag = body.find("meta", property="twitter:image")
        if tag is not None:
            image = tag['content']
        
        # Remove html tags from description
        return image