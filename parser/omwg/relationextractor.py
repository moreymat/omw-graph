#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Extract relation (Hyponyms, Hypernyms, Synonyms) from nltk only for English omw
"""

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '29-03-2014'


import sys
from nltk.corpus import wordnet

out = None


def createWordList(data):
    wordlist = []

    for key in data.keys():
        values = data[key]
        for value in values:
            wordlist.append((key, str(value)))

    return wordlist


def getSynsets(word):
    return wordnet.synsets(word)


def getHyponyms(syn):
    return syn.hyponyms()


def getHypernyms(syn):
    return syn.hypernyms()


def getId(syn):
    i = ""
    padding = ""
    offset = str(syn.offset())

    for i in range(8 - len(offset)):
        padding = padding + "0"

    offset = padding + offset
    offset = offset + "-" + syn.pos()

    return offset

def getName(syns):
    syno = []
    for s in syns:
        for l in s.lemma_names():
            name = s.name().split('.')[0]
            syno.append((getId(s), l))
    return syno



def relations(w1, w2, rtype, lng):
    global out
    deliminator = '_'
    out.write(str(w1[0]) + deliminator + str(w1[1]) + deliminator + lng + "\t" + str(w2[0]) + deliminator + str(w2[1]) + deliminator + lng + "\t" + rtype + "\n")


def getWord(t):
    return getValue(t)


def english(t):
    key, word = t
    syns = getSynsets(word)
    syno = getName(syns)
    for s in syno:
        relations(t, s, 'SYNO', 'eng')

    for syn in syns:
        hypos = getHyponyms(syn)
        hypolemma = getName(hypos)
        for h in hypolemma:
            relations(t, h, 'HYPO', 'eng')
        hyper = getHypernyms(syn)
        hyperlemma = getName(hyper)
        for h in hyperlemma:
            relations(t, h, 'HYPER', 'eng')


def extractRelation(t, lng, header=True):
    global out
    filename = "csv_files/rels-" + lng + ".csv"

    out = open(filename, 'w')
    if header:
        out.write('name:string:key\tname:string:key\ttype\n')
    out.close()
    out = open(filename, 'a')
    if lng == 'eng':
        english(t)
    out.close()


def main():
    directory = sys.argv[1]
    extractRelation(directory)

if __name__ == '__main__':
    main()
