#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '14-04-2014'


def cleanWord(word):
    return word.replace("_", " ")


def indexWord(word):
    #return word.replace("_", "_")
    return word


def writeHeaderRels(target):
    target.write("name:string:key\tname:string:key\ttype\n")


def writeHeaderWord(target):
    target.write("name:string:key\tsynset\tword\n")


def writeLineRels(syn1, word1, syn2, word2, rel, lng, target):
    target.write("{syn1}#{word1}#{lng}\t{syn2}#{word2}#{lng}\t{rel}\n".format(
        syn1=syn1, word1=indexWord(word1), syn2=syn2, word2=indexWord(word2), rel=rel, lng=lng))


def writeLineWord(syn, word, lng, target):
    target.write("{syn}#{wordIndex}#{lng}\t{wordClean}\t{syn}\t{lng}\n".format(
        syn=syn, wordIndex=indexWord(word), wordClean=cleanWord(word), lng=lng))


def hyperRels(wn, hyper, lng, f):
    for key in hyper.keys():
        for g in wn[key]:
            for g2 in hyper[key]:
                for w in wn[g2]:
                    writeLineRels(key, g, g2, w, 'HYPER', lng, f)
                    writeLineRels(g2, w, key, g, 'HYPO', lng, f)
