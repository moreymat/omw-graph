#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" Parse all file in a directory and convert them to a csv file
"""

import os
import sys
import collections
from simplefileparser import parseFile
from simplefileparser import getKey
from simplefileparser import getValue

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '26-03-2014'

dico = None


def getDico():
    """ return the dictionnary
    """
    global dico
    return dico


def filesFromDir(directory):
    """ list the file from a given directory
        return a list of filename
    """
    files = list([])
    for f in os.listdir(directory):
        path = directory + f
        files.append(path)
    return files


def addDico(data):
    """ Add a value to a key in the dictionnary
    """
    global dico

    for d in data:
        key, value = d
        dico[key].append(value)


def parseFiles(files, w):
    """ parse all file in the filename list
    """
    for f in files:
        print(f)
        data = parseFile(f, write=w)
        addDico(data)


def parseDirectory(directory, write=True):
    """ check if the directory exist and
        parse all the file from the directory
    """
    global dico
    dico = collections.defaultdict(list)

    if not(os.path.isdir(directory)):
        print(directory + " : does not exist")
        sys.exit(-1)
    print ("========= Parse " + directory + " =========")
    files = filesFromDir(directory)
    parseFiles(files, write)


def main():
    parseDirectory('../../data/')

if __name__ == '__main__':
    main()
