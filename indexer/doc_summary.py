import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
nltk.download('stopwords')
stopwords = stopwords.words('english')
remove_terms = ['the', '``', "''", "'d", "'ll", "'re", "'s", "'ve", 'could', 'might', 'must', "n't", 'need', 'sha', 'wo', 'would']
stopwords = stopwords + remove_terms + list(string.punctuation)
lemmatizer = nltk.WordNetLemmatizer()


def document_summary(doc, summary_length=1.3):
    sentences = sent_tokenize(doc)
    total_documents = len(sentences)
    freq_matrix = sentence_frequency_matrix(sentences, stopwords)
    tf_matrix = sentence_tf_matrix(freq_matrix)
    df_matrix = sentence_df_matrix(freq_matrix)
    idf_matrix = sentence_idf_matrix(freq_matrix, df_matrix, total_documents)
    tf_idf_matrix = sentence_tf_idf_matrix(tf_matrix, idf_matrix)
    sentence_scores = score_sentences(tf_idf_matrix)
    threshold = calc_average_score(sentence_scores)

    return generate_summary(sentences, sentence_scores, summary_length * threshold)


def sentence_frequency_matrix(sentences, stopWords):
    frequency_matrix = {}
    lem = lemmatizer

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)

        for word in words:
            word = lem.lemmatize(word.lower())

            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def sentence_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}
        count_words_in_sentence = len(f_table)

        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def sentence_df_matrix(freq_matrix):
    df_matrix = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():

            if word in df_matrix:
                df_matrix[word] += 1
            else:
                df_matrix[word] = 1

    return df_matrix


def sentence_idf_matrix(freq_matrix, df_matrix, total_documents):
    import math
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(df_matrix[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def sentence_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, tf_table), (sent2, idf_table) in zip(tf_matrix.items(), idf_matrix.items()):
        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(tf_table.items(), idf_table.items()):  # keys are same: word1 == word2
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def score_sentences(tf_idf_matrix):
    sentence_scores = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        try:
            sentence_scores[sent] = total_score_per_sentence / count_words_in_sentence

        except:
            sentence_scores[sent] = total_score_per_sentence / 1e-7

    return sentence_scores


def calc_average_score(sentence_scores):
    import numpy as np
    sumValues = 0

    for entry in sentence_scores:
        sumValues = np.sum(sentence_scores[entry])
        
    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentence_scores))

    return average


def generate_summary(sentences, sentence_scores, threshold):
    #Can optimize using .join()
    summary = ''

    for sentence in sentences:
        if sentence[:15] in sentence_scores and sentence_scores[sentence[:15]] >= (threshold):
            summary += " " + sentence

    return summary