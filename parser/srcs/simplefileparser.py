#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Simple tab file parser
"""

import os
import sys

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '25-03-2014'


dtl = [] #Data type we want
ccl = [] #Comment char for tab file
deli = '' # delimitor for tabfile
fout = None #output file
headerdone = False


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




def parseLine(line):
    """ Check if the line is commented
        if not extract the key and the value from the line and
        return it as a tuple (key, value)
    """
    global deli

    if line[0] in ccl:
        return
    else:
        sl = line.split(deli)
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


def toCSV(data, output='word.csv', csvdel='\t'):
    global fout
    global headerdone
    fout = open(output, 'a')

    if not(headerdone):
        fout.write('key' + csvdel + 'word\n')
        headerdone = True

    for d in data:
        fout.write(str(d[0]) + csvdel + str(d[1]) +"\n")

    fout.close()

def parseFile(filename='', output='word.csv', delimitor='\t',
              commentcharlist=['#'],
              datatypelist=['lemma', 'fre:lemma'], write=True):
    print("WRITE : " + str(write))

    """ parse a file and return the data extract in a list of tuples """

    data = []
    setVariable(delimitor, commentcharlist, datatypelist)
    f = openFile(filename)
    for line in f:
        kv = parseLine(line)
        if kv is not None:
            data.append(kv)
    if write:
        toCSV(data)
    return data


def main():
    filename = '../data/wn-data-eng.tab'
    data = parseFile(filename)


if __name__ == '__main__':
    main()
