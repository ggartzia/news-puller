import os
import requests
import news_puller.config as cfg
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv()

def news_update(media):
    api_url = os.getenv('HOST_URL') + 'fetch/' + media
    response = requests.get(api_url)

scheduler = BackgroundScheduler()

media = cfg.PAPER_LIST.values()
minute = round(60 / len(media))
start_at = 0

for plist in media:
    scheduler.add_job(lambda: news_update(plist['paper']), CronTrigger(minute=str(start_at), timezone='UTC'))
    start_at += minute

scheduler.start()
