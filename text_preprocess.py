import re
import nltk
from nltk.corpus import stopwords

def query_preprocess(filepath="query.ohsu.1-63"):
    f = open(filepath, 'r')
    lines = f.readlines()

    query = None
    qlist = []

    for i, l in enumerate(lines):
        if "<top>" in l:
            query = dict()
        elif "</top>" in l:
            qlist.append(query)
        elif "<num>" in l:
            query["num"] = l.split("Number: ")[1][:-1]
        elif "<title>" in l:
            t = l.split("> ")[1][:-1].lower()
            if "with" in t: t = t.split("with")[1] # test
            t = t.replace("/", " ")
            query["title"] = t
        elif "<desc>" in l:
            d = lines[i+1][:-1].lower()
            d = d.replace("/", " ")
            query["desc"] = d
        else: pass

        #if i > 10: break

    #for j in qlist: print(j)

    return qlist


def stopword_removal(text, SW):

    t1 = re.sub(r'[^\w\s\/]', '', text)
    text = re.sub(r'\/', ' ', t1)

    text = text.split(" ")
    res = ""

    for token in text:
        if token not in SW:
            res += "%s "%token

    return res[:-1]



if __name__ == "__main__":

    nltk.download("stopwords")

    SW = set(stopwords.words('english'))

    text1 = "Are there adverse effects on lipids, when progesterone EA/ED is given with estrogen replacement therapy?"
    text2 = "infiltrative small bowel processes, information about small bowel lymphoma and heavy alpha chain disease"

    punc = '''!()-[]{};:'"\/,<>.?@#$%^&*_~'''

    t3 = re.sub(r'[^\w\s\/]', '', text1)
    print(t3)
    t4 = re.sub(r'\/', ' ', t3)
    print(t4)

    t1 = stopword_removal(text1, SW)
    t2 = stopword_removal(text2, SW)

    print(t1)
    print(t2)
