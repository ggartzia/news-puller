from news_puller.db.new import num_paper_news, last_new
from news_puller.db.media import select_theme_media
from logging import getLogger, DEBUG

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

def get_media(theme):
    total = []

    try:
        media = select_theme_media(theme)

        for plist in media:
            plist['numeroNoticias'] = num_paper_news(plist['paper'])
            plist['actualizacion'] = last_new(plist['paper'])

            total.append(plist)

    except Exception as e:
        logger.error(e)
        logger.error('There was an error trying to get the data')
        
    return total
