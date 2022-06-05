from logging import getLogger, DEBUG
from nltk import sent_tokenize, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SpanishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


STOP_WORDS = set(stopwords.words('spanish'))
STEMMER = SpanishStemmer()


def tokenize_and_stem(text):
    print('OMG Stemmer')
    toktok = ToktokTokenizer()
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in toktok.tokenize(sent):
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [STEMMER.stem(t) for t in filtered_tokens]
    print('OMG Stemmer %s', stems)
    return stems


def get_topics(corpus):
    words = []
    try:
        print('Garaziiiiiii tfidf 1')
        vec = TfidfVectorizer(stop_words=STOP_WORDS,
                              use_idf=True, 
                              tokenizer=tokenize_and_stem,
                              ngram_range=(1,3)).fit(corpus)
        print('Garaziiiiiii tfidf 2')
        bag_of_words = vec.transform(corpus)
        print('Garaziiiiiii tfidf %s', bag_of_words)
        sum_words = bag_of_words.sum(axis=0)
        print('Garaziiiiiii tfidf %s', sum_words)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        print('Garaziiiiiii tfidf %s', words_freq)
        words = words_freq[:10]
    except Exception as e:
        logger.error('Failed counting words in article. Error: %s', e)

    print('Garaziiiiiii DONE %s', words)
    return words
