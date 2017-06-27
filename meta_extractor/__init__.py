from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.snowball import FrenchStemmer
import nltk


class HistExtractor:
    def __init__(self):
        self.stemmer = FrenchStemmer()
        self.analyzer = CountVectorizer().build_analyzer()

        self.bad_words = ["src", 'html', 'ifram',
                          'allowtransparency', 'analytic', 'class',
                          'com', 'hidden', 'lien', 'lightwidget', 'overflow',
                          'row', 'script', 'scrolling', 'src', 'widget', "tous", "jour", "blog",
                          'width', 'wrapp', "les", "googl", "propos", "list", "https", "être",
                          "plus", "tout"]
        self.stopwords = nltk.corpus.stopwords.words('french') + self.bad_words

        def stemmed_words(doc):
            return (self.stemmer.stem(w) for w in self.analyzer(doc) if w not in self.stopwords)

        self.cv = CountVectorizer(analyzer=stemmed_words, stop_words=self.stopwords)
        # self.cv = CountVectorizer(stop_words=self.stopwords)

    def get_histogram_from_string(self, x):
        hist = self.cv.fit_transform([x])
        dict_result = {k: int(v) for k, v in zip(self.cv.get_feature_names(), hist.toarray()[0]) if
                       k not in self.stopwords and len(k)>2}
        return dict_result
