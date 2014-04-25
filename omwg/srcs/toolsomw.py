#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '25-04-2014'


def cleanWord(word):
    return word.replace("_", " ")


def writeHeaderRels(target):
    target.write("name:string:synkey\tname:string:synkey\ttype\n")


def writeHeaderWord(target):
    target.write("name:string:lexkey\tlemma\tpartofspeech\ttype:label\n")


def writeHeaderSynset(target):
    target.write("name:string:synkey\ttype:label\n")


def writeHeaderRelSynLex(target):
    target.write("name:string:synkey\tname:string:lexkey\ttype\n")


def writeLineRels(syn1, syn2, rel, target):
    target.write("{syn1}\t{syn2}\t{rel}\n".format(
        syn1=syn1, syn2=syn2, rel=rel))


def writeLineWord(lng, version, lex, lemma, pos, target):
    target.write("{key}\t{lemma}\t{pos}\tLexicalEntry\n".format(
        key=lng + '-' + version + '-' + lex,
        lemma=lemma,
        pos=pos))


def writeLineSynset(syn, target):
    target.write("{syn}\tSynset\n".format(syn=syn))


def writeLineRelSynLex(lex, lng, version, syn, target):
    target.write("{syn}\t{lex}\tlexical\n".format(
        syn=syn,
        lex=lng + '-' + version + '-' + lex))
