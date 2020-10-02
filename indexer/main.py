def findWholeWord(w):
    import re
    return re.compile(r'\b({0})'.format(w), flags=re.IGNORECASE).findall

def highlight_term(id, term, text):
    terms = findWholeWord(term)(text)
    for term in terms:
        replaced_text = text.replace(term, "\033[1;32;40m{term}\033[0;0m".format(term=term))
        title = replaced_text.partition('\n')[0]
        final_text = replaced_text.replace(title, "\033[1;31;40m{title}\033[0;0m".format(title=title))
    return "--- document {id}: {replaced}".format(id=id, replaced=final_text)

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

def index_corpus(index):
    import os
    import time

    COLLECTION_DIR = './dataset/tech/'
    files = [COLLECTION_DIR + file for file in os.listdir(COLLECTION_DIR)]

    start = time.time()
    corpus = load_collection(files)
    num_docs = len(corpus)
    doc_freqs = index.doc_freq(corpus)
    for doc_id, text in corpus:
        document = {
            'id': doc_id,
            'text': text
        }
        index.build_index(document, num_docs, doc_freqs)
    end = time.time()
    print('\033[1;36;40m Indexing time: \033[0;0m', end - start)
    index.save_index()

    #index.get_index(1)

def query_collection(index, db, get_docs=False):
    import time
    import nltk
    lemmatizer = nltk.WordNetLemmatizer()
    search_term = input("Enter term(s) to search: ").lower()
    if search_term in ['quit()', 'exit()']:
        exit(0)

    search_term = lemmatizer.lemmatize(search_term)
    start = time.time()
    result = index.lookup_query(search_term)
    end = time.time()
    print('\033[1;36;40m Search time: \033[0;0m', end - start)
    
    start = time.time()
    for term in result.keys():
        for appearance in result[term]:
            document = db.get(appearance[0])
            print('Document: ', appearance[0], ' Term found: ', term ,' Score: ', '{:.5f}'.format(appearance[1]))
            if get_docs:
                print(highlight_term(appearance[0], term, document['text']))
        print("-----------------------------")    
    end = time.time()
    print('\033[1;36;40m Retrieval time: \033[0;0m', end - start)

def main(create_index=False):
    from DocCollection import DocCollection
    from InvertedIndex import InvertedIndex
    db = DocCollection()
    index = InvertedIndex(db)

    if create_index:
        index_corpus(index)
    else:
        try:
            index.load_index_from_file('./indexer/inverted_index.txt')
        except FileNotFoundError:
            print('Must create and save Inverted Index first!')
            user_input = input('Do you want to create Inverted Index now? y/n\n')
            if user_input.lower() == 'y':
                print('Indexing Documents . . .')
                index_corpus(index)
            else:
                exit(0)

    while(True):
        query_collection(index, db, get_docs=False) # get_docs cannot be True if create_index is False
    
main(create_index=False)