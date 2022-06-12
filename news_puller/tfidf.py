import re
import spacy
from logging import getLogger, DEBUG
from news_puller.utils import clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sentiment_analysis_spanish import sentiment_analysis
from nltk.corpus import stopwords

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TfIdfAnalizer(object):

    def __init__(self):
        try:
            self.STOP_WORDS = set(stopwords.words('spanish'))
            self.NLP = spacy.load('en_core_web_sm')
        except: # If not present, we download
            spacy.cli.download('en_core_web_sm')
            self.NLP = spacy.load('en_core_web_sm')


    def get_topics(self, corpus, size=6):
        words = []
        try:
            vec = TfidfVectorizer(stop_words=self.STOP_WORDS,
                                  tokenizer=self.tokenize_stem,
                                  ngram_range=(1,2)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
            words = [w[0] for w in words_freq[:size]]

        except Exception as e:
            logger.error('Failed counting words in article. Error: %s', e)

        return words


    def tokenize_stem(self, text):
        tokens = []
        doc = self.NLP(text)
        for token in doc:
            if re.search('[a-zA-Z]', token.text) and token.text not in self.STOP_WORDS:
                if token.pos_ in ('NOUN', 'PROPN'):
                    tokens.append(token.text)
                elif token.pos_ in ('ADJ', 'ADV', 'VERB'):
                    tokens.append(token.lemma_)

        return tokens


    def count_polarity_words(self, text):
        rate = 0
        try:
            sentiment = sentiment_analysis.SentimentAnalysisSpanish()
            rate = 10 * sentiment.sentiment(text)

            if rate < 4:
                return 'negative'
            elif rate < 7:
                return 'neutral'
            else:
                return 'positive'

        except Exception as e:
            logger.error('Failed analysing sentiment of tweet. Error: %s', e)


    def rate_feeling(self, text):
        try:
            text = clean_html(text)
            return self.count_polarity_words(text)
            
        except Exception as e:
            logger.error('There was an error analysing the text of the tweet: %s', e)
