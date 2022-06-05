from logging import getLogger, DEBUG
import pymongo
from news_puller.db import Database

media_db = Database.DATABASE['media']

def search_media(id):
    media = media_db.find_one({'_id': id})
    
    return media


def select_all_media():
    media = media_db.find({})

    return list(media)


def select_theme_media(theme):
    media = media_db.find({'theme': theme})

    return list(media)