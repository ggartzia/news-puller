from logging import getLogger, DEBUG
from apscheduler.schedulers.background import BackgroundScheduler
from news_puller.fetch import get_news
from news_puller.shares import get_sharings
from news_puller.fake_news import fact_check

log = getLogger('werkzeug')
log.setLevel(DEBUG)


def twitter_update():
    log.debug('twitter_update!')
    response = get_sharings()


def news_update():
    # Fetch the last time it was executed and fetch only the news after that time
    log.debug('news_update!')
    response = get_news()


def fact_check():
    # Fetch the last time it was executed and fetch only the news after that time
    log.debug('fact_check!')
    response = fact_check()


scheduler = BackgroundScheduler()
scheduler.add_job(news_update, 'interval', hours=1)
scheduler.add_job(twitter_update, 'interval', minutes=5)
scheduler.add_job(fact_check, 'interval', hours=5)
scheduler.start()

