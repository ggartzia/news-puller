import csv
import nltk
from logging import getLogger, DEBUG
from nltk import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from news_puller.utils import clean_html


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TfIdfAnalizer(object):

    def __init__(self):
        self.STOP_WORDS = set(stopwords.words('spanish'))
        self.read_lexico_file()
        self.stemmer = SnowballStemmer('spanish')
        self.tokenizer = TweetTokenizer().tokenize


    def tokenize_and_stem(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [self.stemmer.stem(t) for t in filtered_tokens]
        return stems


    def get_topics(self, corpus, size=6):
        words = []
        try:
            vec = TfidfVectorizer(stop_words=self.STOP_WORDS,
                                  tokenizer=self.tokenize_and_stem,
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
        topics = self.get_topics([text], 20)

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
