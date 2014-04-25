#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""LMF Parser
"""

import collections
import sys
from toolsomw import writeLineWord
from toolsomw import writeLineRels
from toolsomw import writeLineSynset
from toolsomw import writeLineRelSynLex
from toolsomw import writeHeaderWord
from toolsomw import writeHeaderRels
from toolsomw import writeHeaderSynset
from toolsomw import writeHeaderRelSynLex

lmffile = None
wordcsv = None
relcsv = None
syncsv = None
relsynlexcsv = None
debugmode = False

outputdir = 'data/csv_files/'

synsets = collections.defaultdict(list)
currentword = ''
currentid = ''
currentpos = ''
target = ''
reltype = ''
lng = ''
version = ''

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
    global currentpos

    if debugmode:
        print("In Lemma Tag")
    currentword = line.split('\'')[1]
    currentpos = line.split('\'')[3]
    return lmffile.readline()

def senseTag(line):
    global lmffile
    global currentword
    global currentid
    global synsets
    global lng
    global wordcsv

    if debugmode:
        print("In Sense")
    synset = line.split('\'')[3]

    if not synset in synsets:
        writeLineSynset(synset, "Synset", syncsv)
        synsets[synset].append(synset)
    writeLineRelSynLex(currentid, lng, version, synset, relsynlexcsv)
    return lmffile.readline()

def lexicalEntryTag(line):

    global currentpos
    global currentword
    global currentid
    global syncsv
    global lng
    global version

    if debugmode:
        print("In Lexical Entry")
    if '<Lemma' in line:
        if debugmode:
            print("Go to lemma")
        line = lemmaTag(line)

    writeLineWord(lng, version, currentid, currentword, currentpos, wordcsv)

    while '<Sense' in line:
        if debugmode:
            print("Go to Sense")
        line = senseTag(line)

    return line

def lexiconTag(line):
    global lmffile
    global lng
    global version
    global wordcsv
    global relcsv
    global syncsv
    global outputdir
    global relsynlexcsv
    global nonlexsyncsv

    if debugmode:
        print("In lexicon")
    lng = line.split('\'')[5]
    version = line.split('\'')[9]

    filename = outputdir + 'word-' + lng + '.csv'
    wordcsv = open(filename, 'w')

    filename = outputdir + 'rel-' + lng + '.csv'
    relcsv = open(filename, 'w')

    filename = outputdir + 'syn-' + lng + '.csv'
    syncsv = open(filename, 'w')

    filename = outputdir + 'relsynlex-' + lng + '.csv'
    relsynlexcsv = open(filename, 'w')

    writeHeaderWord(wordcsv)
    writeHeaderRels(relcsv)
    writeHeaderSynset(syncsv)
    writeHeaderRelSynLex(relsynlexcsv)

    return lmffile.readline()

def synsetRelation(line):
    global lmffile
    global currentid
    global target
    global reltype
    global relcsv
    global lng
    global synsets

    if debugmode:
        print("In Synset Relation")
    target = line.split('\'')[1]
    reltype = line.split('\'')[3]

    return lmffile.readline()

def synsetRelationsTag(line):
    global lmffile
    global relcsv
    global syncsv
    global synsets

    if debugmode:
        print("In Synset Relations")
    line = lmffile.readline()
    while '<SynsetRelation' in line:
        if debugmode:
            print("Go to synset relation")
        targetid = line.split('\'')[1]
        reltype = line.split('\'')[3]

        if not currentid in synsets:
            writeLineSynset(currentid, "Synset,Fake", syncsv)
            synsets[currentid].append(currentid)
            if not targetid in synsets:
                writeLineSynset(targetid, "Synset,Fake", syncsv)
                synsets[targetid].append(targetid)
        writeLineRels(currentid, targetid, reltype, relcsv)

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
    global currentid

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
        currentid = line.split('\'')[1]
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
