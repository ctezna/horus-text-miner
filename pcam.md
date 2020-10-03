# [P]
~~~
T0:
    load(text)
    cleanDocuments()
    appearances = {}
    indexTable = {}

T1:
    for term in terms:
        if term.exists() :
            term.getFrequency()
        else:
            term.frequency = 0
        calculateIDF(term)
        appearances.update(term)
    indexTable.update(appearances)
    database.add(terms)

T2:
    cleanSearchTerms()
    terms = []
    results = {}
    for terms in query:
        terms.add(text.id, text.tfidf)
    resultss.update(sort(terms))

Tlast:
    for term in results:
        print(text.id, text.title, text.tfidf, text)
~~~ 

# [C]
![alt_text](docs/pcam/C.PNG "image_tooltip")

# [A]
![alt_text](docs/pcam/A1.PNG "image_tooltip")

![alt_text](docs/pcam/A2.PNG "image_tooltip")

# [M]
![alt_text](docs/pcam/M.PNG "image_tooltip")

