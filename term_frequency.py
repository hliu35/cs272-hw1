from collections import defaultdict
import numpy as np
from numpy.linalg import norm
import re


def generate_term_map(text, process=True):
    termVector = defaultdict(int)
    if process:
        text = text.lower()[:-1]
        text = text.replace("/", " ")
        text = re.sub(r"[^\w\s]", "", text)
        text = text.split()

    for t in text:
        termVector[t] += 1

    termSet = set(termVector.keys())
    return (termSet, termVector)


def getTFArray(Terms, termMapAll, doc_count):
    m = doc_count
    n = len(Terms)

    TermFrequency = np.zeros([m, n])
    docIDs = []

    for i, doc_id in enumerate(termMapAll.keys()):
        docIDs.append(doc_id)
        for j, t in enumerate(Terms):

            termVec = termMapAll[doc_id]
            termCount = 0
            if t in termVec.keys():
                termCount = termVec[t]
            TermFrequency[i, j] = termCount

    return np.log(1+TermFrequency), docIDs


def getIDFArray(TermFrequency, doc_count):
    a1 = np.sum(TermFrequency, axis=0)
    a2 = (doc_count) / (a1 + 1)
    a3 = np.log(a2)
    a3[a3 == np.infty] = 0
    return a3


def getTFIDFArray(TF, IDF):
    m = TF.shape[0]
    idf2 = np.array([IDF]*m)
    ret = np.multiply(TF, idf2)
    return ret


def getSimilarity(docTFIDF, queryTFIDF):
    return np.dot(docTFIDF, queryTFIDF.transpose()) / (norm(docTFIDF) * norm(queryTFIDF))


def topScores(score_col, k):
    idx = np.argpartition(score_col, -k)[-k:]
    idx = idx[np.argsort(score_col[idx])]
    return idx[::-1]