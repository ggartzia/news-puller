import csv
from logging import getLogger, DEBUG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from news_puller.utils import clean_html


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TfIdfAnalizer(object):

    def __init__(self):
        print("start TfIdfAnalizer")
        self.STOP_WORDS = set(stopwords.words('spanish'))
        self.read_lexico_file()


    def get_topics(self, corpus, size=10):
        words = []
        print("Graararaziii hemen dao arazoa ", corpus)
        try:
            vec = TfidfVectorizer(stop_words=self.STOP_WORDS,
                                  ngram_range=(1,2)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
            words = [w[0] for w in words_freq[:size]]

        except Exception as e:
            logger.error('Failed counting words in article. Error: %s', e)

        return words


    def read_lexico_file(self):
        reader = csv.DictReader(open('lexicon.csv'))

        self.WORD_RATING = {}
        for k, v in reader:
            self.WORD_RATING[k] = v


    def count_polarity_words(self, text):
        rate = 0

        # rate emojis
        topics = self.get_topics(text, 20)
        
        if len(topics) > 0:
            for word in topics:
                rate += self.WORD_RATING.get(word, 0)

            rate = rate / len(topics)

        return rate


    def rate_feeling(self, text):
        rate = 0

        try:
            text = clean_html(text)
            rate = self.count_polarity_words(text)
            
        except Exception as e:
            logger.error('There was an error analysing the text of the tweet: %s', e)

        return rate
