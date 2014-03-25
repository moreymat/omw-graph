#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Guieu Christophe, Tallot Adrien"
__date__ = "21-03-2014"

import os
import sys


def getKeyValue(line):

    """Split the line and get the key and the value
        return a tuple wich contain the key and the value
    """
    splitline = line.split("\t")
    key = splitline[0]
    value = splitline[2]

    return (key, str(value))


def addDico(dico, key, value):

    """add value with key in the dictionary"""
    if dico.get(key) is None:
        dico[key] = [value]
    else:
        dico[key].append(value)


def isComment(line):

    """Say if the line begin by a #"""
    if line[0] == '#':
        return True
    else:
        return False


def isLemma(line):
    splitline = line.split("\t")
    if splitline[1] == "lemma":
        return True
    else:
        return False


def isAdmisible(line):
    """Check if the line is admissible ie line is a lemma"""
    if isComment(line) is True:
        return False
    elif not(isLemma(line)) is True:
        return False
    else:
        return True


def removeCR(word):
    """Remove ending carriage return
    """
    return str(word[0:-1])


def protectChar(word):
    """Protect Char in a word for example : מַכָּ"ם => מַכָּ\"ם"""
    if "\"" in word:
        tmp = list(word)
        tmp[tmp.index("\"")] = "\\\""
        word = ''.join(tmp)
    return str(word)


def parseValue(word):
    word = removeCR(word)
    word = protectChar(word)
    return str(word)


def parseFile(simplefile, dico, lng):

    """Parse a file and add it into the dictionary"""
    for line in simplefile:
        if not(isAdmisible(line)):
            continue
        key, value = getKeyValue(line)
        value = parseValue(value)
        value = (value, lng)

        addDico(dico, key, value)


def parseSimpleFile(filename):
    if not(os.path.isfile(filename)):
        print("This file does not exist")
        sys.exit(-1)
    dico = {}
    f = open(filename, 'r')
    lng = os.path.basename(filename).split('.')[0].split('-')[2]
    parseFile(f, dico, lng)

    return dico


def filesFromDir(directory):
    if not(os.path.isdir(directory)):
        print("This directory does not exist")
        sys.exit(-1)

    """List all files from the given directory"""
    filenames = list([])
    for name in os.listdir(directory):
        path = directory + name
        filenames.append(path)

    return filenames


def parseFiles(directory):

    """Parse all files from the given directory"""
    dico = {}
    filenames = filesFromDir(directory)
    for filename in filenames:
        """Getting language's name from the file name"""
        lng = os.path.basename(filename).split('.')[0].split('-')[2]

        simplefile = open(filename, 'r')
        parseFile(simplefile, dico, lng)
    return dico


def main():
    """docstring for main"""
    if sys.argv[1] == "-d":
        dico = parseFiles(sys.argv[2])
    if sys.argv[1] == "-f":
        dico = parseSimpleFile(sys.argv[2])

    print(dico["00001740-n"])

if __name__ == '__main__':
    main()
