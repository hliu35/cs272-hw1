

if __name__ == "__main__":
    infile = open("qrels.ohsu.88-91", 'r')
    ifl = infile.readlines()
    infile.close()
    outfile = open("qrels.proper.ohsu.88-91", 'w')

    for i, l in enumerate(ifl):
        items = l.replace("\n", '').split("\t")
        relevance = 1 if items[2] == "2" else 0
        outstr = "%s  %d  %s  %d"%(items[0], 0, items[1], relevance)
        outfile.write(outstr)
        if i < len(ifl)-1: outfile.write("\n")

    outfile.close()