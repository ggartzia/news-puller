import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from news_puller.db.media import select_all_media

load_dotenv()


class Scheduler(object):

    def __init__(self):
        self.scheduler = BackgroundScheduler()

        self.start()


    def start(self):
        media = select_all_media()

        for start_at in range(0, 59):
            paper = media[start_at % len(media)]['paper']
            self.scheduler.add_job(lambda paper=paper: self.news_update(paper), CronTrigger(minute=start_at, timezone='UTC'))

        self.scheduler.start()


    def news_update(self, paper):
        api_url = os.getenv('HOST_URL') + 'fetch/' + paper
        response = requests.get(api_url)
