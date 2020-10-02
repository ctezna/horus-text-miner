def findWholeWord(w):
    import re
    return re.compile(r'\b({0})'.format(w), flags=re.IGNORECASE).findall

def highlight_term(id, term, text):
    terms = findWholeWord(term)(text)
    for term in terms:
        replaced_text = text.replace(term, "\033[1;32;40m{term}\033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)

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

def index_corpus():
    import os
    import time
    from DocCollection import DocCollection
    from InvertedIndex import InvertedIndex
    db = DocCollection()
    index = InvertedIndex(db)

    COLLECTION_DIR = './dataset/tech/'
    files = [COLLECTION_DIR + file for file in os.listdir(COLLECTION_DIR)]

    start = time.time()
    corpus = load_collection(files)
    num_docs = len(corpus)
    doc_freqs = index.doc_freq(corpus)
    # for doc_id, text in corpus:
    #     document = {
    #         'id': doc_id,
    #         'text': text
    #     }
    #     index.index_document(document)
    for doc_id, text in corpus:
        document = {
            'id': doc_id,
            'text': text
        }
        index.build_index(document, num_docs, doc_freqs)
    end = time.time()
    print('\033[1;32;40m Indexing time: \033[0;0m', end - start)

    #index.get_index(1)

def query_collection():
    import time
    search_term = input("Enter term(s) to search: ")
    start = time.time()
    result = index.lookup_query(search_term)
    end = time.time()
    print('\033[1;32;40m Search time: \033[0;0m', end - start)
    
    start = time.time()
    for term in result.keys():
        for appearance in result[term]:
            document = db.get(appearance.docId)
            print(highlight_term(appearance.docId, term, document['text']))
        print("-----------------------------")    
    end = time.time()
    print('\033[1;32;40m Retrieval time: \033[0;0m', end - start)

def main():
    index_corpus()

    while(True):
        query_collection()
    
main()