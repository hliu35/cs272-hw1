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
import custom_ranking as CR
import text_preprocess as TP
import my_similarity as MS

DISPLAY_COUNT = 50
HEADLESS = True

print_count = 0



if __name__ == "__main__":
    lucene.initVM()
    print(lucene.VERSION)

    # open document file
    filename = "ohsumed.88-91"
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # set the analyzer
    analyzer = StandardAnalyzer()

    # set the similarity config
    selection = input("Select Similarity\n1: Custom\n2: Boolean\n3: Classic\n4: BM25\nEnter selection (default 1): ")
    s = 1 if selection == "" else int(selection)
    similarity_of_choice = [MS.MysteriousSimilarity(), \
                            BooleanSimilarity(), \
                            ClassicSimilarity(), \
                            BM25Similarity()][s-1]
    # Classic: same as TFIDFSimilarity but not an abstract class

    # store the index
    directory = RAMDirectory() # in memory
    # directory = FSDirectory() # in file system

    config = IndexWriterConfig(analyzer)
    config.setSimilarity(similarity_of_choice)
    iwriter = IndexWriter(directory, config)

    flag = None
    text = None
    doc = None
    docID = None
    doc_count = 0

    begintime = time.time()
    print("Indexing documents...")

    # INDEXING
    for i, l, in enumerate(lines):
        #if i > 100: break # TEST
        if l[0] == '.': # commands
            flag = l[1]
            if flag == 'I':
                if i != 0: iwriter.addDocument(doc)
                doc = Document()
                docID = l[3:]
                doc.add(Field(flag, docID, TextField.TYPE_STORED))
                doc_count += 1
        else:
            l = l.lower()
            if flag == "W": l = TP.stopword_removal(l, SW)
            doc.add(Field(flag, l, TextField.TYPE_STORED))

    midtime = time.time()
    print("\nindexed %d in %.2f seconds\n"%(doc_count, midtime - begintime))
    iwriter.close()

    # READING
    ireader = DirectoryReader.open(directory)

    # SEARCHING WITH QUERIES
    isearcher = IndexSearcher(ireader)
    isearcher.setSimilarity(similarity_of_choice) # IndexSearcher.setSimilarity(XXX)

    qlist = TP.query_preprocess() # a list of query
    outfile = open("qhits.ohsu.88-91", "w")

    for q in qlist:
        # parse a simple query that searches for "text"
        title = q["title"]
        description = q["desc"]

        # further process the query
        description = TP.stopword_removal(description, SW)

        # this is BooleanQuery not BooleanSimilarity (from org.apache.lucene.search.similarities.Similarity)
        searching_query = QB.bq_builder(title, description, analyzer)

        # search with query
        hits = isearcher.search(searching_query, DISPLAY_COUNT).scoreDocs
        print_count += len(hits)

        QueryID = q["num"]
        Q0 = "Q0"

        for i, hit in enumerate(hits):
            result = isearcher.doc(hit.doc)
            if not HEADLESS:
                print(result.get("T"))
                print(result.get("W"))
                print("score: %f\n" % hit.score)
            DocID = int(result.get('U')) # or 'I" ?
            Rank = i
            Score = hit.score
            RunID = "tfidf-Both" # fixed for testing

            outfile.write("%s  %s  %s  %s  %.6f  %s\n"%(QueryID, Q0, DocID, Rank, Score, RunID))

    endtime = time.time()
    print("searched: %.2f seconds\n"%(endtime - midtime))
    print("Total query count:", len(qlist))
    print("Displayed hits:", print_count)
    print("Avg hit per query:", print_count/len(qlist))

    outfile.close()
