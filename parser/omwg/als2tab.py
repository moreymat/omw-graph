#!/usr/share/python
# -*- encoding: utf-8 -*-
#
# Extract synset-word pairs, definitions and others from the Albanian Wordnet
#
#

import sys
import codecs
import re, collections
from toolsomw import writeHeaderRels
from toolsomw import writeHeaderWord
from toolsomw import writeLineWord
from toolsomw import writeLineRels


wndata="../data/"
wnname = "Albanet"
wnlang = "als"
wnurl = "http://fjalnet.com/"
wnlicense = "CC BY 3.0"

#
# header
#
outfile = "wn-data-%s.tab" % wnlang
o = codecs.open(outfile, "w", "utf-8" )
log = codecs.open("log", "w", "utf-8" )

o.write("# %s\t%s\t%s\t%s \n" % (wnname, wnlang, wnurl, wnlicense))

###
### mappings
###
#mapdir = "../data/"
#maps = ["wn20-30.adj", "wn20-30.adv", "wn20-30.noun", "wn20-30.verb"]
#pos = {"wn20-30.adj" : "a", "wn20-30.adv" : "r",
#       "wn20-30.noun" : "n", "wn20-30.verb" : "v", }
#map2030 = collections.defaultdict(lambda: 'unknown');
#for m in maps:
#    mf = codecs.open(mapdir + m, "r", "utf-8" )
#    p = pos[m]
#    for l in mf:
#        lst = l.strip().split()
#        fsfrom = lst[0] + "-" + p
#        fsto = sorted([(lst[i+1], lst[i]) for i in range(1,len(lst),2)])[-1][1]
#        ##print "%s-%s\t%s-%s" % (fsfrom, p, fsto, p)
#        map2030[fsfrom] = "%s-%s" % (fsto, p)
#

#
# Data is in the file shqip.xml
#
# But xml parser complains :-)  so back to regexp
#


f = codecs.open(wndata + "albanet.xml", "r", "utf-8" )

synset = ''
lemma = ''
#of20 = unicode()
defid = 0
exid = 0

wn = collections.defaultdict(list)
rel = ['hypernym']
rels = open('csv_files/rels-als.csv', 'w')
writeHeaderRels(rels)

word = open('csv_files/word-als.csv', 'w')
writeHeaderWord(word)

for l in f:
    ##print l, "EOS"
    ### synset
    m = re.search(r"<ID>(.*)</ID>",l.strip())
    if (m):
        synset = m.group(1).strip()[6:]
        defid = 0
        exid = 0
    ### lemma
    m = re.search(r"<LITERAL>(.*)<SENSE>(.*)</SENSE>",l.strip())
    if(m):
        lemma = m.group(1).strip()
        sense = m.group(2).strip()
        wn[synset].append(lemma)
        o.write("%s\t%s:%s\t%s\n" % (synset, wnlang, 'lemma', lemma))
        writeLineWord(synset, lemma, 'als', word)
    ### Definition
    m = re.search(r"<DEF>(.*)</DEF>",l.strip())
    if(m):
        df = m.group(1).strip()
        o.write("%s\t%s:%s\t%d\t%s\n" % (synset, wnlang, 'def', defid, df))
        defid += 1
    ### Example
    m = re.search(r"<USAGE>(.*)</USAGE>",l.strip())
    if(m):
        ex = m.group(1).strip()
        o.write("%s\t%s:%s\t%d\t%s\n" % (synset, wnlang, 'exe', exid, ex))
        exid += 1
    ### Relations
    m = re.search(r"<TYPE>(.*)</TYPE>(.*)</ILR>", l)
    if(m):
        reltype = str(m.group(1).strip())
        if reltype in rel:
           key = m.group(2).strip()[6:]
           writeLineRels(synset, lemma, key, wn[key], 'HYPER', 'als', rels)
           writeLineRels(key, wn[key], lemma, synset, 'HYPO', 'als', rels)
           #print(lemma + " : " + reltype + " : " + str(wn[key]))

for key in wn.keys():
    for w1 in wn[key]:
        for w2 in wn[key]:
            if w1 == w2:
                continue
            writeLineRels(key, w1, key, w2, 'SYNO', 'als', rels)

rels.close()
