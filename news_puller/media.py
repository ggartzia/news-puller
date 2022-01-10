import news_puller.config as cfg
from news_puller.db import Database

def get_media(theme):
    total = []
    media = filter(lambda m: m['theme'] == theme, cfg.PAPER_LIST)

    for plist in media:
        plist['numeroNoticias'] = Database.num_news({'paper': plist['paper'], 'theme': theme})
        plist['actualizacion'] = Database.last_new(plist['paper'], theme)
        
        total.append(plist)

    return total
