import lucene
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanClause, BooleanQuery
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParserBase


def bq_builder(title, description, analyzer, desc_fields="all"):

    # field A
    #parser_A = QueryParser("T", analyzer) #title parser
    #query_raw_A = description
    #query_A = parser_A.parse(query_raw_A)

    # field B
    #parser_B = QueryParser("M", analyzer) #body parser
    #query_raw_B = description
    #query_B = parser_B.parse(query_raw_B)

    # multi-field query C and more
    #query_C = mfQueryParser(['W', 'M'], description, analyzer)
    #query_C = mfQueryParser(['T', 'W'], title+" "+description, analyzer)
    query_C = mfQueryParser(['T', 'W', 'M'], description, analyzer)

    #query_D = mfQueryParser(["M"], title, analyzer)

    # field E
    #parser_E = QueryParser("W", analyzer)  # body parser
    #query_raw_E = description
    #query_E = parser_B.parse(query_raw_E)


    # boolean combine
    bquery = BooleanQuery.Builder()
    #bquery.add(query_A, BooleanClause.Occur.SHOULD) # SHOULD vs MUST
    #bquery.add(query_B, BooleanClause.Occur.MUST)
    bquery.add(query_C, BooleanClause.Occur.MUST)
    #bquery.add(query_D, BooleanClause.Occur.SHOULD)
    #bquery.add(query_E, BooleanClause.Occur.SHOULD)

    bq_built = bquery.build()

    return bq_built


def mfQueryParser(fields, query_raw, analyzer):
    ''' returns a parsed query ready for search'''
    parser = MultiFieldQueryParser(fields, analyzer)
    #parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    parser.setDefaultOperator(QueryParserBase.OR_OPERATOR)
    #query = parser.parse(query_raw)
    query = MultiFieldQueryParser.parse(parser, query_raw)
    return query
