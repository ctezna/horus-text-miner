class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        from TextPreprocessor import TextPreprocessor
        self.index = dict()
        self.db = db
        self.preprocessor = TextPreprocessor()
    def __repr__(self):
        """
        String representation of the Inverted Index object
        """
        return str(self.index)
        
    def index_document(self, document):
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
            
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
            
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
    
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        for term in query.split(' '):
            if term in self.index:
                return { term: self.index[term] }
            else:
                return {}
        #return { term: self.index[term] for term in query.split(' ') if term in self.index }