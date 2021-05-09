import math
import lucene

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
from org.apache.lucene.search.similarities import SimilarityBase
from org.apache.lucene.index import Term
from org.apache.lucene.search import \
    BooleanClause, BooleanQuery, Explanation, PhraseQuery, TermQuery, ScoreMode
from org.apache.lucene.util import Version
from org.apache.pylucene.search.similarities import PythonClassicSimilarity


class MysteriousSimilarity(PythonClassicSimilarity):

    def lengthNorm(self, numTerms):
        return 1.0

    def tf(self, freq):
        return math.pow(freq, 0.33)

    def idf(self, docFreq, numDocs):
        #return math.log(1 + (numDocs - docFreq + 1)/(docFreq + 1))
        return math.pow(1 + math.log((numDocs - docFreq + 1) / (docFreq + 1)), 2)
        #return math.pow(1+ math.log(numDocs / (docFreq+1)), 2)

    def idfExplain(self, collectionStats, termStats):
        return Explanation.match(1.0, "inexplicable", [])

    def sloppyFreq(self, dist):
        return dist

    def coord(self, q, d):
        return math.pow(q / d, 2)

if __name__ == "__main__":
    lucene.initVM()
    print(lucene.VERSION)

    analyzer = StandardAnalyzer()

    # set the similarity config
    similarity_of_choice = MysteriousSimilarity()

    # store the index
    directory = RAMDirectory()  # in memory
    # directory = FSDirectory() # in file system

    config = IndexWriterConfig(analyzer)
    config.setSimilarity(similarity_of_choice)
    iwriter = IndexWriter(directory, config)