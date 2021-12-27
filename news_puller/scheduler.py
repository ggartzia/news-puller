from logging import getLogger, DEBUG
import requests
import news_puller.config as cfg
from apscheduler.schedulers.background import BackgroundScheduler


log = getLogger('werkzeug')
log.setLevel(DEBUG)


def news_update(theme):
    print('news_update for ' + theme + ' media!')
    api_url = cfg.HOST_URL + 'fetch/' + theme
    response = requests.get(api_url)


def twitter_update():
    print('Update the number of times a new was shared on twitter')
    api_url = cfg.HOST_URL + 'update_twitter_counts/24'
    response = requests.get(api_url)


scheduler = BackgroundScheduler(timezone="Europe/Berlin")
scheduler.add_job(lambda: news_update('noticias'), 'interval', hours=1)
scheduler.add_job(lambda: news_update('deportes'), 'interval', hours=2)
scheduler.add_job(lambda: news_update('corazon'), 'interval', hours=5)
scheduler.add_job(twitter_update, 'interval', minutes=5)


scheduler.start()
