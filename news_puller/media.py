import news_puller.config as cfg
from news_puller.db import Database

def get_media(theme):
    total = []
    media = filter(lambda m: m['theme'] == theme, cfg.PAPER_LIST)

    for plist in media:
        plist['numeroNoticias'] = Database.num_news(plist['paper'], theme)
        print("We have look at numeroNoticias. Value: " + str(plist['numeroNoticias']))
        plist['actualizacion'] = Database.last_new(plist['paper'], theme)
        print("We have look at ultima actualizacion. Value: " + str(plist['actualizacion']))
        
        total.append(plist)

    return total
