class TextPreprocessor:
    """
    Text preprocessing class
    """
    def __init__(self):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer 
        stopwords   -- list of ignored words
        """
        import nltk
        from nltk.corpus import stopwords
        nltk.download('stopwords')
        self.stopwords = stopwords.words('english')
        self.remove_terms = ['the', '``', "''"]
        self.lemmatizer = nltk.WordNetLemmatizer()

    def preprocess(self, document):
        from nltk.tokenize import word_tokenize
        import string
        words = word_tokenize(document)
        words_clean = []
        for word in words: # Go through every word in your tokens list
            w = word.lower()
            if (w not in self.stopwords and w not in string.punctuation and w not in self.remove_terms):  # remove stopwords and punctuation
                words_clean.append(self.lemmatizer.lemmatize(w))
        return words_clean