#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Simple tab file parser
"""

import os
import sys

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '25-03-2014'
__version__ = '0.1'


dtl = []
ccl = []
deli = ''


def getKey(t):
    """ Return the key of a tuple"""
    return t[0]


def getValue(t):
    """ return the value of a tuple"""
    return t[1]


def verifyFile(filename):
    """ Verify the file """
    if filename == '':
        print('Error : put filename')
        sys.exit(-1)
    elif not(os.path.isfile(filename)):
        print('Error : put a valid filename')
        sys.exit(-1)


def openFile(filename=''):
    """ Open a file wich the name is given"""
    try:
        f = open(filename, 'r')
    except IOError as ioe:
        print("Error in " + __file__ + " : " + "can not open " + filename)
        sys.exit(-1)
    else:
        return f



def removeCR(word):
    """ Remove ending carriage return"""
    return str(word[0:-1])


def protectChar(word):
    """ protect specify char with a \ """
    if '"' in word:
        lw = list(word)
        lw[lw.index('"')] = '\\"'
        word = ''.join(lw)
    return str(word)


def removeSpace(word):
    return word.replace(' ', '_')


def parseWord(word):
    """ Remove the carriage return and protect the char
        return the word as a string
    """
    word = removeCR(word)
    word = protectChar(word)
    word = removeSpace(word)
    return str(word)


def splitLine(line):
    """ Split the line with the given delimitor """
    global deli
    return line.split(deli)


def parseLine(line):
    """ Check if the line is commented
    if not extract the key and the value from the line and
    return it as a tuple (key, value)
    """
    if line[0] in ccl:
        return
    else:
        sl = splitLine(line)
        if not(sl[1] in dtl):
            return
        word = parseWord(str(sl[2]))
        key = sl[0]
        return (key, str(word))


def setVariable(delimitor='\t',
                commentcharlist=['#'],
                datatypelist=['lemma']):
    """ Set global virables """
    global dtl
    global ccl
    global deli

    dtl = datatypelist
    ccl = commentcharlist
    deli = delimitor


def parseFile(filename='', delimitor='\t',
              commentcharlist=['#'],
              datatypelist=['lemma', 'fre:lemma']):

    """ parse a file and return the data extract in a list of tuples """

    data = []
    setVariable(delimitor, commentcharlist, datatypelist)
    f = openFile(filename)
    for line in f:
        kv = parseLine(line)
        if kv is not None:
            data.append(kv)
    return data


def main():
    filename = '../data/wn-data-eng.tab'
    data = parseFile(filename)


if __name__ == '__main__':
    main()
