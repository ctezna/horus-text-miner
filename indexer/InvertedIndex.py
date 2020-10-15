class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        from TextPreprocessor import TextPreprocessor
        self.index = dict()
        self.db = db
        self.preprocessor = TextPreprocessor()
        self.output_file = './indexer/inverted_index.txt'


    def _doc_freq(self, corpus):
        from gensim import corpora
        docs = [self.preprocessor.preprocess(doc) for docid, doc in corpus]
        dictionary = corpora.Dictionary(docs)
        dfs = {}
        for key, value in dictionary.token2id.items():
            dfs[key] = dictionary.dfs[value]
        return dfs

    def doc_freq(self, corpus):
        from gensim import corpora
        import pymp
        pymp.config.nested = False
        pymp.config.thread_limit = 4
        docs = pymp.shared.list()
        with pymp.Parallel(4) as p:
            for index in p.range(0, len(corpus)):
                docs.append(self.preprocessor.preprocess(corpus[index][1]))
        dictionary = corpora.Dictionary(docs)
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
        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            idf = self.calc_idf(term, num_docs, doc_freqs[term])
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1, idf)
            
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }

        self.index.update(update_dict)

        # Add the document into the database
        self.db.add(document)

        return document


    def load_db(self, document):
        self.db.add(document)

        return document


    def get_index(self, n):
        print(list(self.index.items())[:n])


    def load_index_from_file(self, file):
        import json

        f = open(file)
        raw = f.read()
        self.index = json.loads(raw)
        f.close()


    def save_index(self):
        import json
        from Appearence import AppearanceEncoder

        with open(self.output_file, 'w') as file:
            file.write(json.dumps(self.index, cls=AppearanceEncoder))


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

        result = {}

        for term in query.split(' '):
            if term in self.index:
                term_arr = []

                for t in self.index[term]:
                    try:
                        term_arr.append((t.docId, t.tfidf))

                    except:
                        term_arr.append((t['docId'], t['tfidf']))
                result.update({ term: sorted(term_arr, key=itemgetter(1)) })
                
        return result
        #return { term: self.index[term] for term in query.split(' ') if term in self.index } aun funciona?