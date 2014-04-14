#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '14-04-2014'


def writeHeaderRels(target):
    target.write("name:string:key\tname:string:key\ttype")


def writeHeaderWord(target):
    target.write("name:string:key\tsynset\tword")


def writeLineRels(syn1, word1, syn2, word2, rel, lng, target):
    target.write("{syn1}#{word1}#{lng}\t{syn2}#{word2}#{lng}\t{rel}".format(
        syn1=syn1, word1=word1, syn2=syn2, word2=word2, rel=rel, lng=lng))


def writeLineWord(syn, word, lng, target):
    target.write("{syn}#{word}#{lng}\t{word}".format(
        syn=syn, word=word, lng=lng))
