#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def getKeyValue(line):
    """plit the line and get the key and the value"""
    splitline = line.split("\t")
    key = splitline[0]
    value = splitline[2]

    return (key, value)

def addDico(dico, key, value):
    """add value with key in the dictionary"""
    if dico.get(key) == None:
        dico[key] = [value]
    else:
        dico[key].append(value)

def isComment(line):
    """Say if the line begin by a #"""
    if line[0] == '#':
        return True
    else:
        return False

def parseFile(simplefile, dico):
    """Parse a file and add it into the dictionary"""
    for line in simplefile:
        if isComment(line) == True:
            continue
        key, value = getKeyValue(line)
        value = (value, simplefile.name.split('.')[1].split('-')[2])
        addDico(dico, key, value)

def filesFromDir(directory):
    """List all the files in the given directory"""
    filenames = list([])
    for name in os.listdir(directory):
        path = directory + name
        filenames.append(path)

    return filenames

def parseFiles(directory):
    """Parse all the file from the given directory"""
    dico = {}
    filenames = filesFromDir(directory)
    for filename in filenames:
        simplefile = open(filename, 'r')
        parseFile(simplefile, dico)
    return dico


def main():
    """docstring for main"""
    dico = parseFiles("./data/")
    print(dico["00001740-n"])

if __name__ == '__main__':
    main()
