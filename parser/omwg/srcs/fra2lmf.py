#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
"""

import re, sys
import collections

fra = open('wolf-1.0b4.xml', 'r')
lmf = open('wolf-1.0b4-lmf.xml', 'w')

wid = 0
word2synset = collections.defaultdict(list)

for line in fra:
    synsetite = re.search(r'<ID>eng-30-(.*-[avnrb])<\/ID>', line)
    if synsetite:
        synset = synsetite.group(1).strip().replace('-b', '-r')
    wordite = re.finditer(r'<LITERAL[^>]*>([^<]+)<', line)
    for word in wordite:
        word = word.group(1).strip()
        word2synset[word].append(synset)

compteur = 0
for word in word2synset.keys():
    le = "<LexialEntry id='" + str(compteur) + "'>\n"
    compteur = compteur + 1
    lemma = "\t<Lemma writtenForm='" + str(word) + "' partOfSpeech='" + word2synset[word][0][-1] + "'/>\n"
    lmf.write(le)
    lmf.write(lemma)
    for s in word2synset[word]:
        senseid = str(compteur) + "_" + s
        sense = "\t<Sense id='" + senseid + "' synset='" + s + "'/>\n"
        lmf.write(sense)

    lef = "</LexialEntry>\n"
    lmf.write(lef)


fra.close()
lmf.close()
