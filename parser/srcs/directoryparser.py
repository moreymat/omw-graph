#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Parse all file in a directory
"""

import os
import sys
from simpleFileParser import parseFile
from simpleFileParser import getKey
from simpleFileParser import getValue

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '26-03-2014'
__version__ = '0.1'

dico = {}


def getDico():
    """ return the dictionnary """
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
    """ Add a value to a key in the dictionnary if the key exist,
    else create the entry and set it to the value
    """
    global dico

    for d in data:
        key = getKey(d)
        value = getValue(d)

        if dico.get(key) is None:
            dico[key] = [value]
        else:
            dico[key].append(value)


def parseFiles(files):
    """ parse all file in the filename list """
    for f in files:
        print(f)
        data = parseFile(f)
        addDico(data)


def parseDirectory(directory):
    """ check if the directory exist and
    parse all the file from the directory """
    if not(os.path.isdir(directory)):
        print(directory + " : does not exist")
        sys.exit(-1)
    print ("========= Parse " + directory + " =========")
    files = filesFromDir(directory)
    parseFiles(files)


def main():

    global dico

    directory = raw_input("Entrer the data directory : ")

    parseDirectory(directory)


if __name__ == '__main__':
    main()
