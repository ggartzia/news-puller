import pandas as pd
import spacy
import math
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

class TfIdfAnalizer(object):

    def __init__(self):
        try:
            self.RUSSEL = {
                270 : 'relax',
                180 : 'sad',
                90 : 'angry',
                0 : 'happy'
            }
            self.STOP_WORDS = set(stopwords.words('spanish'))
            self.LEXICON = pd.read_csv('lexicon.txt', sep='\t', header= 0)
            self.LEXICON['Spanish-es'] = self.LEXICON['Spanish-es'].astype(str)
            
            spacy.cli.download('es_core_news_sm')
            self.NLP = spacy.load('es_core_news_sm')

        except Exception as e:
            logging.error('Failed downloading spacy client. Error: %s', e)


    def get_topics(self, title, description, text):
        words = []
        corpus = [title, description] + text
        try:
            vec = TfidfVectorizer(stop_words=self.STOP_WORDS,
                                  tokenizer=self.tokenize_lemmatize,
                                  ngram_range=(1,2),
                                  use_idf=False).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
            words = [w[0] for w in words_freq[:10]]

        except Exception as e:
            logging.error('Failed counting words in article. Error: %s', e)

        return words


    def tokenize_lemmatize(self, text):
        tokens = []
        doc = self.NLP(text)
        for token in doc:
            if token.pos_ in ('ADJ', 'NOUN') and token.text not in self.STOP_WORDS:
                tokens.append(token.lemma_)

        return tokens


    def getRusselRegion(self, arousal, valence):
        result = 'none'
        a = math.atan2(arousal - 5, valence - 5)
        mydegrees = math.degrees(a)
        deg = mydegrees if mydegrees > 0 else mydegrees + 360

        for x in self.RUSSEL.keys():
            if deg > x:
                result = self.RUSSEL[x]
                break

        if valence == 0:
            result = 'none'

        return result


    def getRussellValues(self, tweet):
        valence = 0
        arousal = 0

        try:
            doc = self.NLP(tweet)
            lis = [str(token) for token in doc if not str(token) in self.STOP_WORDS]
            b = self.LEXICON[self.LEXICON['Spanish-es'].isin(lis)]
            for i, r in b.iterrows():
                valence += r['Valence']
                arousal += r['Arousal']
        
            return self.getRusselRegion(arousal, valence)

        except Exception as e:
            logging.error('Failed analysing emotions of tweet. Error: %s', e)
