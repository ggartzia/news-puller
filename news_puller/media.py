import news_puller.config as cfg
from news_puller.db import Database
from logging import getLogger, DEBUG

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

def get_media(theme):
    total = []
    media = filter(lambda m: m['theme'] == theme, cfg.PAPER_LIST.values())

    try:
        for plist in media:
            plist['numeroNoticias'] = Database.num_news(plist['paper'], theme)
            plist['actualizacion'] = Database.last_new(plist['paper'], theme)

            total.append(plist)

    except Exception as e:
        logger.error(e)
        logger.error('There was an error trying to get the data')
        
    return total
