import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from news_puller.db.media import select_all_media

load_dotenv()


def news_update(paper):
    api_url = os.getenv('HOST_URL') + 'fetch/' + paper
    response = requests.get(api_url)


scheduler = BackgroundScheduler()

media = select_all_media()
job = 0

for start_at in range(0, 60):
	paper = media[job]['paper']
    scheduler.add_job(lambda paper=paper: news_update(paper), CronTrigger(minute=start_at, timezone='UTC'))
    job = 0 if job == len(media) else job++

scheduler.start()
