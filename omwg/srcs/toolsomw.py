#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '14-04-2014'


def writeHeaderRels(target):
    target.write("name:string:key\tname:string:key\ttype\n")


def writeHeaderWord(target):
    target.write("name:string:key\tsynset\tword\n")


def writeLineRels(syn1, word1, syn2, word2, rel, lng, target):
    target.write("{syn1}#{word1}#{lng}\t{syn2}#{word2}#{lng}\t{rel}\n".format(
        syn1=syn1, word1=word1, syn2=syn2, word2=word2, rel=rel, lng=lng))


def writeLineWord(syn, word, lng, target):
    target.write("{syn}#{word}#{lng}\t{word}\n".format(
        syn=syn, word=word, lng=lng))

def hyperRels(wn, hyper, lng, f):
    for key in hyper.keys():
        for g in wn[key]:
            for g2 in hyper[key]:
                for w in wn[g2]:
                    g = str(g).replace(" ", "_")
                    w = str(w).replace(" ", "_")
                    writeLineRels(key, g, g2, w, 'HYPER', lng, f)
                    writeLineRels(g2, w, key, g, 'HYPO', lng, f)
