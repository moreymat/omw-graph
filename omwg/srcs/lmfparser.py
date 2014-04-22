#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""LMF Parser
"""

import collections
import sys, re
from toolsomw import writeLineWord
from toolsomw import writeLineRels
from toolsomw import writeHeaderWord
from toolsomw import writeHeaderRels


lmffile = None
wordcsv = None
relcsv  = None
debugmode = False

outputdir = '../data/csv_files/'

word = collections.defaultdict(list) # key : synset value: word
currentword = ''
currentid = ''
target = ''
reltype = ''
lng = ''


def globalInformationTag(line):
    global lmffile
    if debugmode:
        print("In Global Information")
    while '<!--' in line:
        line = lmffile.readline()
    return line

def lemmaTag(line):
    global lmffile
    global currentword
    if debugmode:
        print("In Lemma Tag")
    currentword = line.split('\'')[1]

    return lmffile.readline()

def senseTag(line):
    global lmffile
    global currentword
    global word
    global lng
    global wordcsv

    if debugmode:
        print("In Sense")
    synset = line.split('\'')[3]
    pos = synset.split('-')[3]
    nu = synset.split('-')[2]
    synset = nu + '-' + pos
    writeLineWord(synset, currentword, lng, wordcsv)
    word[synset].append(currentword)
    return lmffile.readline()

def lexicalEntryTag(line):
    if debugmode:
        print("In Lexical Entry")
    if '<Lemma' in line:
        if debugmode:
            print("Go to lemma")
        line = lemmaTag(line)
    while '<Sense' in line:
        if debugmode:
            print("Go to Sense")
        line = senseTag(line)

    return line

def lexiconTag(line):
    global lmffile
    global lng
    global wordcsv
    global relcsv
    global outputdir

    if debugmode:
        print("In lexicon")
    lng = line.split('\'')[5]

    filename = outputdir + 'word-'+ lng + '.csv'
    wordcsv = open(filename, 'w')

    filename = outputdir + 'rel-'+ lng + '.csv'
    relcsv = open(filename, 'w')

    writeHeaderWord(wordcsv)
    writeHeaderRels(relcsv)

    return lmffile.readline()

def synsetRelation(line):
    global lmffile
    global currentid
    global target
    global reltype
    global word
    global relcsv
    global lng

    if debugmode:
        print("In Synset Relation")
    target = line.split('\'')[1]
    pos = target.split('-')[3]
    nu = target.split('-')[2]
    target = nu + '-' + pos
    reltype = line.split('\'')[3]
    for w in word[currentid]:
        for w2 in word[target]:
            writeLineRels(currentid, w, target, w2, reltype, lng, relcsv)

    return lmffile.readline()

def synsetRelationsTag(line):
    global lmffile
    if debugmode:
        print("In Synset Relations")
    line = lmffile.readline()
    while '<SynsetRelation' in line:
        if debugmode:
            print("Go to synset relation")
        line = synsetRelation(line)
    return lmffile.readline()

def statementTag(line):
    global lmffile
    return lmffile.readline()

def definitionTag(line):
    global lmffile
    line = lmffile.readline()
    while '<Statement' in line:
        line = statementTag(line)

    return lmffile.readline()

def synsetTag(line):
    global lmffile
    global currentid
    if debugmode:
        print("In Synset")
    currentid = line.split('\'')[1]
    pos = currentid.split('-')[3]
    nu = currentid.split('-')[2]
    currentid = nu + '-' + pos
    line = lmffile.readline()

    if '<Definition' in line:
        if debugmode:
            print("Go to definition")
        line = definitionTag(line)

    if '<SynsetRelations>' in line:
        if debugmode:
            print("Go to synsetRelations")
        line = synsetRelationsTag(line)

    return lmffile.readline()

def lexicalRessourceTag(line):
    global lmffile
    if debugmode:
        print("In lexical Ressource")
    if '<GlobalInformation' in line:
        if debugmode:
            print("Go to globalInformation")
        line = globalInformationTag(lmffile.readline())
    if '<Lexicon' in line:
        if debugmode:
            print("Go lexicon")
        line = lexiconTag(line)

    while '<LexicalEntry' in line:
        if debugmode:
            print("Go to lexical Entry")
        line = lexicalEntryTag(lmffile.readline())
        if '</LexicalEntry>' in line:
            line = lmffile.readline()

    while '<Synset id=' in line:
        if debugmode:
            print("Go to Synset")
        line = synsetTag(line)

    return line

def main():
    global debugmode
    global wordcsv
    global relcsv
    global lmffile

    filenameoutput = sys.argv[1]
    lmffile = open(filenameoutput, 'r')
    line = lmffile.readline()
    while line:
        if '<LexicalResource>' in line:
            if debugmode:
                print("Go to lexicalRessource")
            line = lexicalRessourceTag(lmffile.readline())
        if '</LexicalResource>' in line:
            if debugmode:
                print("End")
            return
        else:
            line = lmffile.readline()

if __name__ == '__main__':
    main()
