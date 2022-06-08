import csv
from logging import getLogger, DEBUG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from news_puller.utils import clean_html


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

STOP_WORDS = set(stopwords.words('spanish'))
WORD_RATING = read_lexico_file()

def get_topics(corpus, size=10):
    words = []
    try:
        vec = TfidfVectorizer(stop_words=STOP_WORDS,
                              ngram_range=(1,2)).fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        words = [w[0] for w in words_freq[:size]]

    except Exception as e:
        logger.error('Failed counting words in article. Error: %s', e)

    return words


def read_lexico_file():
    with open('lexicon.csv', newline=';') as f:
        return csv.DictReader(f, skipinitialspace=True)


def count_polarity_words(text):
    rate = 0
    text = clean_html(text)
    topics = get_topics(text, 20)

    for ngram in topics:

        if WORD_RATING[word] is not None:
            rate += WORD_RATING[word]

    return rate / len(topics)


def rate_feeling(text):
    rate = 0

    try:
        rate = count_polarity_words(text)
        print("Texxttttt: %s. Rate: %s", text, rate)
        
    except Exception as e:
        logger.error('There was an error analysing the text of the tweet: %s', e)

    return rate
