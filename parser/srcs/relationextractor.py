#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Extract relation (Hyponyms, Hypernyms, Synonyms) from nltk
"""

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '29-03-2014'


from simplefileparser import parseFile
from nltk.corpus import wordnet


def createWordList(data):
    wordlist = []

    for t in data:
        wordlist.append(str(t[1]))

    return wordlist


def getSynsets(word):
    return wordnet.synsets(word)


def getHyponyms(syn):
    return syn.hyponyms()


def getHypernyms(syn):
    return syn.hypernyms()


def getName(syns):
    syno = []
    for s in syns:
        for l in s.lemma_names():
            syno.append(l)
    return syno


def synonyms(w1, w2):
# connec to neo4j
    print(str(w1) + " SYNO " + str(w2))


def hyponyms(w1, w2):
# connec to neo4j
    print(str(w1) + " HYPO " + str(w2))


def hypernyms(w1, w2):
# connec to neo4j
    print(str(w1) + " HYPER " + str(w2))


def relations(w1, w2, rtype):
    if rtype == 'SYNO':
        synonyms(w1, w2)
    elif rtype == 'HYPO':
        hyponyms(w1, w2)
    elif rtype == 'HYPER':
        hypernyms(w1, w2)


def main():
    data = parseFile('../data/wn-data-eng.tab')

    wordlist = createWordList(data)

    for word in wordlist:
        syns = getSynsets(word)
        syno = getName(syns)
        for s in syno:
            relations(word, s, 'SYNO')


        for syn in syns:
            hypos = getHyponyms(syn)
            hypolemma = getName(hypos)


        for syn in syns:
            hyper = getHypernyms(syn)
            hyperlemma = getName(hyper)


if __name__ == '__main__':
    main()
