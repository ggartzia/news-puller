import news_puller.config as cfg
from logging import getLogger, DEBUG
import requests
import argparse
import re
from nltk.tokenize import RegexpTokenizer
from news_puller.db import Database

log = getLogger('werkzeug')
log.setLevel(DEBUG)


def sanitize(sentence):
    sentence = sentence.strip().replace('-19', '')
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+||\-+')
    tokens = tokenizer.tokenize(sentence)
    sentence = " ".join([token.lower().strip() for token in tokens])
    sentence = re.sub(r'[ ]+',' ', sentence)
    sentence = sentence.replace('  ', ' ')
    return sentence


def get_verdicts(question):
    query = {'query': question, 'key': GOOGLE_API_KEY}
    response = requests.get(GOOGLE_API_URL, params=query, headers={'Content-Type':'application/json'})

    if response.status_code != 200:
        log.debug('DID NOT WORK!')

    else:
        resp_json = response.json()
        fact, verdict = [], []

        for claim in resp_json['claims']:
            sentence = sanitize(claim['text'])
            fact.append(sentence)

            for review in claim['claimReview']:
                verdict.append(review['textualRating'])

        #res_scores = get_true_false(verdict)
        res = []
        for i in range(len(fact)):
            cur_res = (fact[i],
            	       #res_scores[i],
            	       verdict[i])
            res.append(cur_res)

        return res


def fact_check():
    news = Database.select_last_news(48)

    for new in news:
    	parser = argparse.ArgumentParser()
    	parser.add_argument("q", help=new['title'], type=str)
    	args = parser.parse_args()

    	fakes = get_verdicts(args.q)

    ##Database.update('news', fakes)

    return fakes