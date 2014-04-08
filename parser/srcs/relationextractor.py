#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Extract relation (Hyponyms, Hypernyms, Synonyms) from nltk only for English omw
"""

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '29-03-2014'


import sys
from directoryparser import parseDirectory
from directoryparser import getDico
from simplefileparser import getValue
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



def relations(w1, w2, rtype):
    global out
    out.write(str(w1[0]) + str(w1[1]) + "\t" + str(w2[0]) + str(w2[1]) + "\t" + rtype + "\n")

def getWord(t):
    return getValue(t)


def extractRelation(directory):
    """Extract the relation for English Omw
    """
    global out

    parseDirectory(directory, write=False)
    data = getDico()
    wordlist = createWordList(data)

    out = open('rels.csv', 'a')
    out.write('name:string:key\tname:string:key\ttype\n')

    for t in wordlist:
        word = getWord(t)
        syns = getSynsets(word)
        syno = getName(syns)
        for s in syno:
            relations(t, s, 'SYNO')

        for syn in syns:
            hypos = getHyponyms(syn)
            hypolemma = getName(hypos)
            for h in hypolemma:
                relations(t, h, 'HYPO')


        for syn in syns:
            hyper = getHypernyms(syn)
            hyperlemma = getName(hyper)
            for h in hyperlemma:
                relations(t, h, 'HYPER')



def main():
    directory = sys.argv[1]
    extractRelation(directory)

if __name__ == '__main__':
    main()
