import nltk
import os, time
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English
 
class Index:
    """ Inverted index datastructure """
 
    def __init__(self, tokenizer, stemmer=None, stopwords=None):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer 
        stopwords   -- list of ignored words
        """
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)
 
    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)
 
        return [self.documents.get(id, None) for id in self.index.get(word)]
 
    def add(self, document, doc_id):
        """
        Add a document string to the index
        """
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue
 
            if self.stemmer:
                token = self.stemmer.stem(token)
 
            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)
 
        #self.documents[self.__unique_id] = document
        self.documents[self.__unique_id] = doc_id
        self.__unique_id += 1


    def get_index(self):
        print(self.index)



def load_document(file):
    f = open(file)
    try:
        raw = f.read()
        return file.split('/')[-1], raw
    except:
        print(file)
        pass

def load_collection(files):
    texts = []
    for file in files:
        doc_id, text = load_document(file)
        texts.append((doc_id, text))
    return texts

if __name__ == "__main__":
    COLLECTION_DIR = './dataset/tech/'
    index = Index(nltk.word_tokenize, 
              EnglishStemmer(), 
              nltk.corpus.stopwords.words('english'))
    files = [COLLECTION_DIR + file for file in os.listdir(COLLECTION_DIR)]

    corpus = load_collection(files)
    for doc_id, text in corpus:
        index.add(text, doc_id)

    while(True):
        query = input()
        #index.get_index()
        start = time.time()
        relevant_docs = index.lookup(query)
        print(relevant_docs)
        end = time.time()
        print(end - start)