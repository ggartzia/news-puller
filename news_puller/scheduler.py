import requests
import news_puller.config as cfg
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def news_update(theme):
    print('news_update for ' + theme + ' media!')
    api_url = cfg.HOST_URL + 'fetch/' + theme
    response = requests.get(api_url)


def twitter_update(theme, period):
    print('Update the number of times a new was shared on twitter')
    api_url = cfg.HOST_URL + 'fetch/' + theme + '/tweetCount/' + str(period)
    response = requests.get(api_url)


scheduler = BackgroundScheduler(timezone="Europe/Berlin")
scheduler.add_job(lambda: news_update('noticias'), CronTrigger(minute='0,30'))
scheduler.add_job(lambda: news_update('deportes'), CronTrigger(minute='15'))
scheduler.add_job(lambda: news_update('corazon'), CronTrigger(minute='45'))

scheduler.start()
