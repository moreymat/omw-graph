#!/usr/share/python
# -*- encoding: utf-8 -*-
#
# Extract synset-word pairs from the Princeton Wordnet
# Replace '_' with ' '

import codecs
from toolsomw import *

from nltk.corpus import wordnet as w

#wndata="/home/bond/svn/wnja/tab/"
wnname = "Princeton WordNet"
wnlang = "eng"
wnurl = "http://wordnet.princeton.edu/"
wnlicense = "wordnet"

#
# functions
#


def createSynset(offset, pos):
    synset = "%08d-%s" % (offset, pos)
    if synset.endswith('s'):
        synset = synset[:-1] + 'a'
    return synset



#
# header
#

outfile_rels = open('data/csv_files/rels-eng.csv', 'w')
outfile_word = open('data/csv_files/word-eng.csv', 'w')

#
# main
#

for s in w.all_synsets():
    synset = createSynset(s.offset(), s.pos())
    lemmas = s.lemmas()

    for l in s.lemmas():
        writeLineWord(synset, l.name(), wnlang, outfile_word)
        for k in s.lemmas():
            if k != l:
                writeLineRels(synset, l.name(), synset, k.name(), 'SYNO', wnlang, outfile_rels)

    hyper = s.hypernyms()
    for h in hyper:
        synsethyper = createSynset(h.offset(), h.pos())
        for lh in h.lemmas():
            for l in lemmas:
                writeLineRels(synsethyper, lh.name(), synset, l.name(), 'HYPER', wnlang, outfile_rels)

    hypo = s.hyponyms()
    for h in hypo:
        synsethypo = createSynset(h.offset(), h.pos())
        for lh in h.lemmas():
            for l in lemmas:
                writeLineRels(synsethypo, lh.name(), synset, l.name(), 'HYPO', wnlang, outfile_rels)

outfile_rels.close()
