import news_puller.config as cfg
from logging import getLogger, DEBUG
from news_puller.db import Database

log = getLogger('werkzeug')
log.setLevel(DEBUG)


def get_media(theme):
    total = []
    media = filter(lambda m: m['theme'] == theme, cfg.PAPER_LIST)

    for plist in media:
        print('Fetch ' + plist['paper'] + ' news from ' + plist['feed'])

        plist['numeroNoticias'] = Database.num_news(plist['paper'], theme)
        plist['actualizacion'] = Database.last_new(plist['paper'], theme)

    return total
