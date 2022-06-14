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

        if search_new(new_id) is None:

            page = requests.get(url)
            if (page.status_code == 200):

                soup = BeautifulSoup(page.text, 'html.parser')

                title = soup.find("meta", property="og:title")
                description = soup.find("meta", name="description")
                topics = self.TFIDF.get_topics([title + ' ' + description])
                media = search_media(paper)

                new = {'id': new_id,
                       'fullUrl': url,
                       'title': title,
                       'description': description,
                       'paper': media['_id'],
                       'theme': media['theme'],
                       'published': utils.parse_date(soup.find("meta", property="article:published_time")),
                       'topics': topics,
                       'image': soup.find("meta", property="twitter:image")
                      }
                
                save_topics(topics, theme)
                save_new(new)

                return new_id
        else:
            return new_id

        return None