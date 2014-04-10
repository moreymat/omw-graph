#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" Parse all file in a directory and convert them to a csv file
"""

import os
import sys
import collections
from tabtocsv import parseFile

__author__ = 'Guieu Christophe, Tallot Adrien'
__date__ = '26-03-2014'


def filesFromDir(directory):
    """ list the file from a given directory
        return a list of filename
    """
    files = list([])
    for f in os.listdir(directory):
        path = directory + f
        files.append(path)
    return files




def parseFiles(files, w):
    """ parse all file in the filename list
    """
    for f in files:
        print(f)
        parseFile(f)


def parseDirectory(directory, write=True):
    """ check if the directory exist and
        parse all the file from the directory
    """

    if not(os.path.isdir(directory)):
        print(directory + " : does not exist")
        sys.exit(-1)
    print ("========= Parse " + directory + " =========")
    files = filesFromDir(directory)
    parseFiles(files, write)


def main():
    directory = sys.argv[1]
    parseDirectory(directory)

if __name__ == '__main__':
    main()
