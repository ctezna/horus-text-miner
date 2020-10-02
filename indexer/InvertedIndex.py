class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        from TextPreprocessor import TextPreprocessor
        self.index = dict()
        self.df_counts = dict()
        self.db = db
        self.preprocessor = TextPreprocessor()
    def __repr__(self):
        """
        String representation of the Inverted Index object
        """
        return str(self.index)

    def doc_freq(self, corpus):
        from gensim import corpora
        import nltk
        dictionary = corpora.Dictionary(self.preprocessor.preprocess(doc) for docid, doc in corpus)
        dfs = {}
        for key, value in dictionary.token2id.items():
            dfs[key] = dictionary.dfs[value]
        return dfs

    def build_index(self, document, num_docs, doc_freqs):
        """
        Process a given document, save it to the DocCollection and update the index.
        """
        from Appearence import Appearance
        terms = self.preprocessor.preprocess(document['text'])
        
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms: #term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            if term in appearances_dict:
                term_frequency = appearances_dict[term].frequency
            else:
                term_frequency = 0
            
            idf = self.calc_idf(term, num_docs, doc_freqs[term])
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1, idf)
            
        update_dict = {}
        for (key, appearance) in appearances_dict.items():
            if key not in self.index:
                update_dict[key] = [appearance]
            else:
                update_dict[key] = self.index[key] + [appearance]
        
        # Update the inverted index
        # update_dict = { key: [appearance]
        #                if key not in self.index
        #                else self.index[key] + [appearance]
        #                for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    def get_index(self, n):
        print(list(self.index.items())[:n])

    def calc_idf(self, term, num_docs, doc_freq):
        import numpy as np
        idf = np.log((1 + num_docs) / (1 + doc_freq)) + 1
        return idf
    
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        from operator import itemgetter
        for term in query.split(' '):
            if term in self.index:
                term_arr = []
                for t in self.index[term]:
                    term_arr.append((t.docId, t.tfidf))
                #return { term: self.index[term] }
                return { term: sorted(term_arr, key=itemgetter(1)) }
            else:
                return {}
        #return { term: self.index[term] for term in query.split(' ') if term in self.index }