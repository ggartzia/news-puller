import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from news_puller.db import Database

load_dotenv()

scheduler = BackgroundScheduler()

media = Database.select_all_media()
minute = round(60 / len(media))
start_at = 0

for plist in media:
    api_url = os.getenv('HOST_URL') + 'fetch/' + plist['paper']
    scheduler.add_job(lambda: requests.get(api_url), CronTrigger(minute=start_at, timezone='UTC'))
    start_at += minute

scheduler.start()
