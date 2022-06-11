from logging import getLogger, DEBUG
from news_puller.utils import clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
import spacy

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TfIdfAnalizer(object):

    def __init__(self):
        self.NLP = spacy.load("es_core_news_sm")


    def get_topics(self, corpus, size=6):
        words = []
        try:
            vec = TfidfVectorizer(tokenizer=self.tokenizer,
                                  ngram_range=(1,3)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
            words = [w[0] for w in words_freq[:size]]

        except Exception as e:
            logger.error('Failed counting words in article. Error: %s', e)

        return words


    def tokenizer(text):
        tokens = []
        doc = NLP(text)
        print(doc.text)
        for token in doc:
            print(token.text, token.pos_, token.dep_)
            print(token.lemma_)
            tokens.append(token.text)

        return tokens


    def count_polarity_words(self, text):
        rate = 0
        return rate * 10


    def rate_feeling(self, text):
        rate = 0

        try:
            text = clean_html(text)
            rate = self.count_polarity_words(text)
            
        except Exception as e:
            logger.error('There was an error analysing the text of the tweet: %s', e)

        return rate
