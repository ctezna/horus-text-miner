class TextPreprocessor:
    """
    Text preprocessing class
    """
    def __init__(self):
        """
        lemmatizer   -- NLTK compatible lemmatize function
        remove_terms -- extra terms to ignore
        stopwords    -- list of ignored words
        """
        import nltk
        from nltk.corpus import stopwords
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        self.stopwords = stopwords.words('english')
        self.remove_terms = ['the', '``', "''"]
        self.lemmatizer = nltk.WordNetLemmatizer()

    def preprocess(self, document):
        """
        Tokenizes documents then normalizes and lemmatizes tokens
        """
        from nltk.tokenize import word_tokenize
        import string
        words = word_tokenize(document)
        words_clean = []
        for word in words: # Go through every word in your tokens list
            w = word.lower()
            if (w not in self.stopwords and w not in string.punctuation and w not in self.remove_terms):  # remove stopwords and punctuation
                words_clean.append(self.lemmatizer.lemmatize(w))
        return words_clean

    def ppreprocess(self, document):
        """
        Tokenizes documents then normalizes and lemmatizes tokens
        """
        from nltk.tokenize import word_tokenize
        import string
        import pymp
        pymp.config.nested = False
        pymp.config.thread_limit = 2
        words = word_tokenize(document)
        words_clean = pymp.shared.list()
        with pymp.Parallel(2) as p:
            for word in p.iterate(words):
                w = word.lower()
                if (w not in self.stopwords and w not in string.punctuation and w not in self.remove_terms):  # remove stopwords and punctuation
                    words_clean.append(self.lemmatizer.lemmatize(w))
        return words_clean