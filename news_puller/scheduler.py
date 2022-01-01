import requests
import news_puller.config as cfg
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def news_update(media):
    print('news_update for ' + media + ' media!')
    api_url = cfg.HOST_URL + 'fetch/' + media
    response = requests.get(api_url)


def twitter_update(theme, period):
    print('Update the number of times a new was shared on twitter')
    api_url = cfg.HOST_URL + 'fetch/' + theme + '/tweetCount/' + str(period)
    response = requests.get(api_url)


scheduler = BackgroundScheduler()
scheduler.add_job(lambda: news_update('elpais'), CronTrigger(minute='5', timezone='UTC'))
scheduler.add_job(lambda: news_update('elmundo'), CronTrigger(minute='10', timezone='UTC'))
scheduler.add_job(lambda: news_update('huffington'), CronTrigger(minute='15', timezone='UTC'))
scheduler.add_job(lambda: news_update('vanguardia'), CronTrigger(minute='20', timezone='UTC'))
scheduler.add_job(lambda: news_update('confidencial'), CronTrigger(minute='25', timezone='UTC'))
scheduler.add_job(lambda: news_update('vanitatis'), CronTrigger(minute='29', timezone='UTC'))
scheduler.add_job(lambda: news_update('publico'), CronTrigger(minute='33', timezone='UTC'))
scheduler.add_job(lambda: news_update('okdiario'), CronTrigger(minute='37', timezone='UTC'))
scheduler.add_job(lambda: news_update('esdiario'), CronTrigger(minute='40', timezone='UTC'))
scheduler.add_job(lambda: news_update('marca'), CronTrigger(minute='43', timezone='UTC'))
scheduler.add_job(lambda: news_update('as'), CronTrigger(minute='48', timezone='UTC'))
scheduler.add_job(lambda: news_update('hola'), CronTrigger(minute='52', timezone='UTC'))
scheduler.add_job(lambda: news_update('lecturas'), CronTrigger(minute='55', timezone='UTC'))
scheduler.add_job(lambda: news_update('diezminutos'), CronTrigger(minute='0', timezone='UTC'))

scheduler.start()
