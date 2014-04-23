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
    target.write("name:string:synkey\tname:string:synkey\ttype\n")


def writeHeaderWord(target):
    target.write("name:string:lexkey\tlemma\tpartofspeech\n")


def writeHeaderSynset(target):
    target.write("name:string:synkey\n")


def writeHeaderRelSynLex(target):
    target.write("name:string:synkey\tname:string:lexkey\ttype\n")


def writeLineRels(syn1, syn2, rel, target):
    target.write("{syn1}\t{syn2}\t{rel}\n".format(
        syn1=syn1, syn2=syn2, rel=rel))


def writeLineWord(lng, version, lex, lemma, pos, target):
    target.write("{key}\t{lemma}\t{pos}\n".format(
        key=lng + '-' + version + '-' + lex,
        lemma=lemma,
        pos=pos))


def writeLineSynset(syn, target):
    target.write("{syn}\n".format(syn=syn))


def writeLineRelSynLex(lex, lng, version, syn, target):
    target.write("{syn}\t{lex}\tlexical\n".format(
        syn=syn,
        lex=lng + '-' + version + '-' + lex))


def hyperRels(wn, hyper, lng, f):
    for key in hyper.keys():
        for g in wn[key]:
            for g2 in hyper[key]:
                for w in wn[g2]:
                    writeLineRels(key, g, g2, w, 'HYPER', lng, f)
                    writeLineRels(g2, w, key, g, 'HYPO', lng, f)
