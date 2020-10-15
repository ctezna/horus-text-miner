def findWholeWord(w):
    import re
    return re.compile(r'\b({0})'.format(w), flags=re.IGNORECASE).findall

def highlight_term(term, text, is_summary=False):
    terms = findWholeWord(term)(text)
    for term in terms:
        replaced_text = text.replace(term, '\033[1;32;40m{term}\033[0;0m'.format(term=term))
        if not is_summary:
            title = replaced_text.partition('\n')[0]
            replaced_text = replaced_text.replace(title, '\033[1;31;40m{title}\033[0;0m'.format(title=title))
        else:
            return replaced_text
    return '{replaced}'.format(replaced=' '.join(replaced_text.partition('\n')[1:]))

def load_document(file):
    with open(file, 'r') as f:
        #f = open(file)
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

    COLLECTION_DIR = './dataset/newDataset/'
    files = [COLLECTION_DIR + file for file in os.listdir(COLLECTION_DIR)]

    start = time.time()
    corpus = load_collection(files)
    end = time.time()
    print('\033[1;36;40m Load collection time: \033[0;0m', end - start)

    num_docs = len(corpus)

    start = time.time()
    doc_freqs = index.doc_freq(corpus)
    end = time.time()
    print('\033[1;36;40m doc_freq time: \033[0;0m', end - start)

    start = time.time()
    for doc_id, text in corpus:
        document = { 'id': doc_id, 'text': text }
        index.build_index(document, num_docs, doc_freqs)
    end = time.time()
    print('\033[1;36;40m Indexing time: \033[0;0m', end - start)
    index.save_index()

def query_collection(index, db, get_docs=False):
    import time
    import nltk
    from doc_summary import document_summary
    COLLECTION_DIR = './dataset/newDataset/'
    lemmatizer = nltk.WordNetLemmatizer()
    search_term = input('Enter term(s) to search: ').lower()
    generate_summary = -1
    if search_term in ['quit()', 'exit()']:
        exit(0)
    if 'summary()' in search_term.split() or 's()' in search_term.split():
        generate_summary = float(input('How long of summaries? (Choose number between 0 and 1, where 0 returns full text.)\n')) * 2
        search_term.replace('summary()', '')
        search_term.replace('s()', '')

    search_term = lemmatizer.lemmatize(search_term)
    start = time.time()
    result = index.lookup_query(search_term)
    end = time.time()
    print('\033[1;36;40m Search time: \033[0;0m', end - start)

    totalDocs = 0
    start = time.time()
    for term in result.keys():
        for appearance in result[term]:
            document = db.get(appearance[0])
            print('\033[1;35;40m'+('Document: '+ appearance[0]+ ' Term found: '+ term +' Score: '+ '{:.5f}'.format(appearance[1])) + '\033[0;0m')
            if get_docs:
                try:
                    text = document['text']
                except:
                    text = load_document(COLLECTION_DIR + appearance[0])[1]
                title = text.partition('\n')[0]
                print('Title: ', '\033[1;31;40m{title}\033[0;0m'.format(title=title))
                if generate_summary > 0:
                    summary = document_summary(text, generate_summary)
                    try:
                        print(highlight_term(term, summary, is_summary=True))
                    except:
                        print('{summary}'.format(summary=summary))
                    # get_full_text = input('See full text? y/n\n')
                    # if get_full_text.lower() in ['y', 'yes']:
                    #     print(highlight_term(appearance[0], term, text))
                else:
                    print(highlight_term(term, text))
                print('\n')
            totalDocs += 1
        print('-----------------------------')    
    end = time.time()
    print('\033[1;36;40m Total documents returned: \033[0;0m', totalDocs)
    print('\033[1;36;40m Retrieval time: \033[0;0m', end - start)

def main(create_index=False):
    import time
    from DocCollection import DocCollection
    from InvertedIndex import InvertedIndex
    db = DocCollection()
    index = InvertedIndex(db)

    if create_index:
        index_corpus(index)
    else:
        try:
            start = time.time()
            index.load_index_from_file('./indexer/inverted_index.txt')
            end = time.time()
            print('\033[1;36;40m Load Index time: \033[0;0m', end - start)
        except FileNotFoundError:
            print('Must create and save Inverted Index first!')
            user_input = input('Do you want to create Inverted Index now? y/n\n')
            if user_input.lower() == 'y':
                print('Indexing Documents . . .')
                index_corpus(index)
            else:
                exit(0)

    while(True):
        query_collection(index, db, get_docs=True)

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main(create_index=True)