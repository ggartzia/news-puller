from logging import getLogger, DEBUG
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

STOP_WORDS = set(stopwords.words('spanish'))

def get_topics(corpus):
    words = []
    try:
        vec = TfidfVectorizer(stop_words=STOP_WORDS,
                              ngram_range=(1,2)).fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        words = [w[0] for w in words_freq[:10]]
    except Exception as e:
        logger.error('Failed counting words in article. Error: %s', e)

    print('Garaziiiiiii DONE %s', words)
    return words
