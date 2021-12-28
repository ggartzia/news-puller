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


def twitter_update(theme, period):
    print('Update the number of times a new was shared on twitter')
    api_url = cfg.HOST_URL + 'fetch/' + theme + '/tweetCount/' + str(period)
    response = requests.get(api_url)


scheduler = BackgroundScheduler(timezone="Europe/Berlin")
#scheduler.add_job(lambda: news_update('noticias'), 'interval', minutes=15)
#scheduler.add_job(lambda: news_update('deportes'), 'interval', minutes=30)
#scheduler.add_job(lambda: news_update('corazon'), 'interval', minutes=60)
#scheduler.add_job(lambda: twitter_update('noticias', 12), 'interval', minutes=15)
#scheduler.add_job(lambda: twitter_update('deportes', 12), 'interval', minutes=20)
#scheduler.add_job(lambda: twitter_update('corazon', 12), 'interval', minutes=30)

scheduler.start()
