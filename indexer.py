import re                                  # library for regular expression operations
import string                              # for string operations
import os
import time

import nltk
from nltk.corpus import stopwords          # module for stop words that come with NLTK
from nltk.tokenize import sent_tokenize, word_tokenize      # tokenizes sentences and words
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


COLLECTION_DIR = './dataset/tech/'
INVERTED_INDEX_FILE = './index/inverted_index.txt'
STOPWORDS_ENGLISH = stopwords.words('english')
REMOVE_TERMS = ['the', '``', "''"]
LEMMATIZER = nltk.WordNetLemmatizer()
freqs = {}

def load_document(file):
    f = open(file)
    try:
        raw = f.read()
        return file.split('/')[-1], raw
    except:
        print(file)
        pass
    

def preprocess(doc):
    words = word_tokenize(doc)
    text = nltk.Text(words)
    words_clean = []

    for word in words: # Go through every word in your tokens list
        w = word.lower()
        if (w not in STOPWORDS_ENGLISH and w not in string.punctuation and w not in REMOVE_TERMS):  # remove stopwords and punctuation
            words_clean.append(LEMMATIZER.lemmatize(w))
    return words_clean


def tf_idf_weighting(text):
    count_vect = CountVectorizer()
    word_vec = count_vect.fit_transform(text)
    tf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True).fit(word_vec)
    x_data = tf_transformer.transform(word_vec)

    df_idf = pd.DataFrame(tf_transformer.idf_, index=count_vect.get_feature_names(),columns=['idf_weights']) 
 
    print(word_vec)
    # sort ascending 
    df_idf.sort_values(by=['idf_weights'])

    return x_data
    
    # for word in text:
    #     if word in freqs:
    #         freqs[word] += 1
    #     else:
    #         freqs[word] = 1    
    # return freqs
        
def load_collection(files):
    texts = []
    for file in files:
        doc_id, text = load_document(file)
        texts.append((doc_id, text))
    return texts


if __name__ == "__main__":
    files = [COLLECTION_DIR + file for file in os.listdir(COLLECTION_DIR)]

    start = time.time()
    corpus = load_collection(files)
    for doc_id, text in corpus:
        tf_idf_weighting(doc_id, text)
    
    end = time.time()
    print(end - start)
    print(len(freqs))
