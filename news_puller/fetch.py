from logging import getLogger, DEBUG
from news_puller.db.new import search_new, save_new
from news_puller.db.media import search_media
from news_puller.db.topic import save_topics
from news_puller.tfidf import TfIdfAnalizer
import news_puller.utils as utils
import feedparser


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class NewsListener(object):

    def __init__(self):
        self.TFIDF = TfIdfAnalizer()

    def get_news(self, paper):
        paper_news = None

        try:
            media = search_media(paper)
            paper_news = feedparser.parse(media['feed'])

            if (paper_news is not None and paper_news.status == 200):
                self.filter_feed(media['theme'], media['paper'], paper_news['entries'])
            else:
                logger.error('Some connection error', paper_news.status)

        except Exception as e:
            logger.error('Failed to load USE model, USE API won\'t be available: %s', e)

        pass


    def filter_feed(self, theme, paper, news):
        # Parse only a given number of news to avoid TimeOut Exception
        for item in news:
            try:
                if bool(item):
                    link = item['link']
                    id = utils.create_unique_id(link)
                    new = search_new(id)

                    if new is None:
                        title = utils.clean_html(item['title'])
                        description = self.get_description(item)
                        topics = self.TFIDF.get_topics([title + ' ' + description])
                        new = {'id': id,
                               'fullUrl': link,
                               'title': title,
                               'description': description,
                               'paper': paper,
                               'theme': theme,
                               'published': utils.parse_date(item['published_parsed']),
                               'topics': topics,
                               'image': self.select_image(item)
                              }

                        save_topics(topics, theme)
                        save_new(new)

            except Exception as e:
                logger.error('Something happened with new: %s. %s', item['link'], e)

        pass


    def select_image(self, new):
        thumb_image = ''

        try:  
            if 'media_thumbnail' in new:
                thumb_image = new['media_thumbnail'][0]['url']
            
            elif 'media_content' in new:
                thumb_image = new['media_content'][0]['url']
         
            elif 'enclosure' in new:
                thumb_image = new['enclosure'][0]['url']

            elif 'links' in new:
                images = list(filter(lambda l: l['rel'] == 'enclosure', new['links']))
                if len(images) > 0:
                    thumb_image = images[0]['href']

        except Exception as e:
            logger.error('Failed getting an image for article %s. Error: %s', new['link'], e)

        return thumb_image


    def get_description(self, new):
        description = ''

        if 'dc_abstract' in new:
            description = new['dc_abstract']
            
        elif 'summary' in new:
            description = new['summary']

        elif 'description' in new:
          description = new['description']
        
        elif 'media_description' in new:
          description = new['media_description']
        
        # Remove html tags from description
        return utils.clean_html(description)
