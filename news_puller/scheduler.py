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


def news_update(paper):
    api_url = os.getenv('HOST_URL') + 'fetch/' + paper
    response = requests.get(api_url)


def create_job(paper):
    scheduler.add_job(lambda: news_update(paper), CronTrigger(minute=start_at, timezone='UTC'))
    start_at += minute
    

funcs = [lambda: create_job(plist['paper']) for plist in media]
for f in funcs: f()

scheduler.start()
