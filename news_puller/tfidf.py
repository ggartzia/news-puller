from logging import getLogger, DEBUG
from news_puller.utils import clean_html
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
#from sentiment_analysis_spanish import sentiment_analysis


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TfIdfAnalizer(object):

    def __init__(self):
        self.STOP_WORDS = set(stopwords.words('spanish'))


    def get_topics(self, corpus, size=6):
        words = []
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


    def count_polarity_words(self, text):
        rate = 0

#        try:
#            sentiment = sentiment_analysis.SentimentAnalysisSpanish()
#            print("rate ------->>>> %s", sentiment.sentiment(text))

#            rate = sentiment.sentiment(text)

#        except Exception as e:

#            logger.error('There was an error running SentimentAnalysisSpanish %s', e)

        return rate * 10


    def rate_feeling(self, text):
        rate = 0

        try:
            text = clean_html(text)
            rate = self.count_polarity_words(text)
            
        except Exception as e:
            logger.error('There was an error analysing the text of the tweet: %s', e)

        return rate
