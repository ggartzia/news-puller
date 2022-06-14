import requests
from news_puller.db.new import save_new

def scrap_new(url):
	page = requests.get(url)
	print("this is the new.. %s", page)
	save_new(page)
	page