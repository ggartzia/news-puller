from news_puller.database import Database

media_db = Database.DATABASE['media']

def search_media(name):
    media = media_db.find_one({'twitter_name': name})
    
    return media


def select_all_media():
    media = media_db.find({})

    return list(media)
