#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def getKeyValue(line):

    """Split the line and get the key and the value"""
    splitline = line.split("\t")
    key = splitline[0]
    value = splitline[2]

    return (key, value)


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


def parseFile(simplefile, dico, lng):

    """Parse a file and add it into the dictionary"""
    for line in simplefile:
        if not(isAdmisible(line)):
            print(line)
            continue
        key, value = getKeyValue(line)
        value = (value, lng)

        addDico(dico, key, value)


def filesFromDir(directory):

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
    dico = parseFiles("../data/")
    print(dico["00001740-n"])

if __name__ == '__main__':
    main()
