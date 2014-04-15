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

outfile_rels = codecs.open('csv_files/rels-eng.csv', 'w')
outfile_word = codecs.open('csv_files/word-eng.csv', 'w')

writeHeaderRels(outfile_rels)
writeHeaderWord(outfile_word)

#
# main
#

for s in w.all_synsets():
    for l in s.lemmas():
        synset = createSynset(s.offset(), s.pos())
        writeLineWord(synset, l.name(), wnlang, outfile_word)
        for k in s.lemmas():
            if k != l:
                writeLineRels(synset, l.name().replace('_',' '), synset, k.name().replace('_',' '), 'SYNO', wnlang, outfile_rels)
outfile_rels.close()
