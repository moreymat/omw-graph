#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Extract relation (Hyponyms, Hypernyms, Synonyms) from nltk only for English omw
"""

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '29-03-2014'


from directoryparser import parseDirectory
from directoryparser import getDico
from simplefileparser import getValue
from nltk.corpus import wordnet


def createWordList(data):
    wordlist = []

    if type(data) is dict:
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


def getName(syns):
    syno = []
    for s in syns:
        for l in s.lemma_names():
            syno.append(l)
    return syno


def synonyms(w1, w2):
# connec to neo4j
    #print(str(w1) + " SYNO " + str(w2))
    pass


def hyponyms(w1, w2):
# connec to neo4j
    #print(str(w1) + " HYPO " + str(w2))
    pass


def hypernyms(w1, w2):
# connec to neo4j
    #print(str(w1) + " HYPER " + str(w2))
    pass


def relations(w1, w2, rtype):
    if rtype == 'SYNO':
        synonyms(w1, w2)
    elif rtype == 'HYPO':
        hyponyms(w1, w2)
    elif rtype == 'HYPER':
        hypernyms(w1, w2)

def getWord(t):
    return getValue(t)

def extractRelation(directory):
    """Extract the relation for English Omw
    """
    parseDirectory(directory)
    data = getDico()
    wordlist = createWordList(data)

    for t in wordlist:
        word = getWord(t)
        syns = getSynsets(word)
        syno = getName(syns)
        for s in syno:
            relations(word, s, 'SYNO')

        for syn in syns:
            hypos = getHyponyms(syn)
            hypolemma = getName(hypos)
            for h in hypolemma:
                relations(word, h, 'HYPO')


        for syn in syns:
            hyper = getHypernyms(syn)
            hyperlemma = getName(hyper)
            for h in hyperlemma:
                relations(word, h, 'HYPER')



def main():
    directory = raw_input("Enter a directory : ")
    extractRelation(directory)

if __name__ == '__main__':
    main()
