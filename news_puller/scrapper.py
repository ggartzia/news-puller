import requests
from bs4 import BeautifulSoup
from news_puller.db.new import save_new

def scrap_new(url):
    page = requests.get(url)
    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, 'html.parser')
        print("this is the new.. %s", soup)
        #save_new(page)
        return True

    else:
        return False