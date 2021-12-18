from logging import getLogger, DEBUG
from apscheduler.schedulers.background import BackgroundScheduler
from news_puller.fetch import get_news

log = getLogger('werkzeug')
log.setLevel(DEBUG)


def news_update():
    # Fetch the last time it was executed and fetch only the news after that time
    log.debug('news_update!')
    response = get_news()


scheduler = BackgroundScheduler()
scheduler.add_job(news_update, 'interval', hours=1)
#scheduler.add_job(twitter_update, 'interval', minutes=5)
#scheduler.add_job(fact_check, 'interval', hours=5)
scheduler.start()

