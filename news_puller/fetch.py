import news_puller.save
import numpy as np
import news_puller.config as cfg
import feedparser
import logging


try:
    for paper in cfg.paper_list:
        logging.debug(paper)
        d = feedparser.parse(paper)

except:
    logging.warning('Failed to load USE model, USE API won\'t be available')


def get_news():
    news = session.run()

    return np.array(news).tolist()
