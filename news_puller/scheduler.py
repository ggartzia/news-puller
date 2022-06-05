import os
import requests
import news_puller.config as cfg
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv()

def news_update(paper):
    api_url = os.getenv('HOST_URL') + 'fetch/' + paper
    response = requests.get(api_url)

scheduler = BackgroundScheduler()

media = cfg.PAPER_LIST.values()
minute = round(60 / len(media))
print('Run every..... ' + str(minute))
start_at = 0

for plist in media:
    print('Create scheduler for:::' + str(plist['paper']) + 'in minute:: ' + str(start_at))
    scheduler.add_job(lambda: news_update(plist['paper']), CronTrigger(minute=start_at, timezone='UTC'))
    start_at += minute

scheduler.start()
