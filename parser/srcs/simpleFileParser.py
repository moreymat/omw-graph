#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Simple File Parser
"""

import os
import sys

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '25-03-2014'
__version__ = '0.1'


dtl = []
ccl = []
deli = ''


def verifyFile(filename):
    if filename == '':
        print('Error : put filename')
        sys.exit(-1)
    elif not(os.path.isfile(filename)):
        print('Error : put a valid filename')
        sys.exit(-1)


def openFile(filename=''):
    verifyFile(filename)
    f = open(filename, 'r')

    return f


def splitLine(line):
    global deli
    return line.split(deli)


def parseLine(line):
    if line[0] in ccl:
        return
    else:
        sl = splitLine(line)
        if not(sl[1] in dtl):
            return
        return (sl[0], sl[2])


def setVariable(delimitor='\t',
                commentcharlist=['#'],
                datatypelist=['lemma']):
    global dtl
    global ccl
    global deli

    dtl = datatypelist
    ccl = commentcharlist
    deli = delimitor


def parseFile(filename='', delimitor='\t',
              commentcharlist=['#'],
              datatypelist=['lemma']):
    data = []
    setVariable(delimitor, commentcharlist, datatypelist)
    f = openFile(filename)
    for line in f:
        kv = parseLine(line)
        data.append(kv)

    return data


def main():
    parseFile('../data/wn-data-heb.tab')

if __name__ == '__main__':
    main()
