import os
import time
import re

import lucene
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
SW = set(stopwords.words('english'))

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import FSDirectory, RAMDirectory
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.document import Document
from org.apache.lucene.document import Field
from org.apache.lucene.document import TextField
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser

from org.apache.lucene.search import ScoreDoc
from org.apache.lucene.search import BooleanClause, BooleanQuery
from org.apache.lucene.search.similarities import BooleanSimilarity, ClassicSimilarity, BM25Similarity
from org.apache.lucene.search.similarities import SimilarityBase

import query_builder as QB
import text_preprocess as TP
import term_frequency as TFQ

DISPLAY_COUNT = 50
HEADLESS = True

print_count = 0


if __name__ == "__main__":
    # open document file
    filename = "ohsumed.88-91"
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    termMapAll = dict()
    queryTermMapAll = dict()
    Terms = set()

    flag = None
    text = None
    doc = None
    docID = None
    uid = None
    doc_count = 0
    UIDs = []

    begintime = time.time()

    N = len(lines)

    # INDEXING
    for i, l, in enumerate(lines):
        if i % 20000 == 0: print("%d out of %d"%(i, N))

        if l[0] == '.': # commands
            flag = l[1]
            if flag == 'I':
                docID = l[3:]
        else:
            if flag == "U":
                uid = int(l)
            elif flag == "W":
                l = TP.stopword_removal(l) # test
                termSet, termMap = TFQ.generate_term_map(l)
                Terms = Terms.union(termSet)
                termMapAll[docID] = termMap
                UIDs.append(uid)
                doc_count += 1
                if doc_count > 10000: break  # TEST

    # Query indexing
    midtime = time.time()
    print("\nindexed %d in %.2f seconds\n" % (doc_count, midtime - begintime))

    # QUERY
    qlist = TP.query_preprocess()  # a list of query
    query_count = len(qlist)
    outfile = open("qhits.ohsu.88-91", "w")

    for q in qlist:
        # parse a simple query that searches for "text"
        num = q["num"]
        title = q["title"]
        description = q["desc"]

        # further process the query
        description = TP.stopword_removal(description, SW)
        dl = description.split(" ")
        termSet, termMap = TFQ.generate_term_map(dl, process=False)
        Terms = Terms.union(termSet)
        queryTermMapAll[num] = termMap


    # obtain numpy tf and idf
    TermFrequency, docIDs = TFQ.getTFArray(Terms, termMapAll, doc_count)
    InverseDocFrequency = TFQ.getIDFArray(TermFrequency, doc_count)
    TFIDF = TFQ.getTFIDFArray(TermFrequency, InverseDocFrequency)

    #print(TermFrequency.shape)
    #print(InverseDocFrequency.shape)
    #print(TFIDF.shape)

    queryTermFrequency, queryIDs = TFQ.getTFArray(Terms, queryTermMapAll, query_count)
    queryInverseDocFrequency = TFQ.getIDFArray(queryTermFrequency, query_count)
    queryTFIDF = TFQ.getTFIDFArray(queryTermFrequency, queryInverseDocFrequency)

    #print(queryTermFrequency.shape)
    #print(queryInverseDocFrequency.shape)
    #print(queryTFIDF.shape)


    # compute cosine similarity
    similarity = TFQ.getSimilarity(TFIDF, queryTFIDF)

    endtime = time.time()
    print("searched: %.2f seconds\n" % (endtime - midtime))
    print("Total query count:", len(qlist))
    print("Displayed hits:", print_count)
    print("Avg hit per query:", print_count / len(qlist))

    # search with query

    Q0 = "Q0"
    k = 50

    for i, qid in enumerate(queryIDs):
        scores = similarity[:, i]
        idx = TFQ.topScores(scores, k)
        top_scores = scores[idx]
        for rank in range(k):
            doc_i = idx[rank]
            RunID = "test"
            outfile.write("%s  %s  %s  %s  %.6f  %s\n"%(qid, Q0, UIDs[doc_i], rank, top_scores[rank], RunID))

    outfile.close()