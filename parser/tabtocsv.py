#!/usr/bin/env python

rels = None
wordout = None
omw = None

dtl = []
ccl = []
deli = ''

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

def appendLine(f, line):
    f.write(line)

def main():
    omw = open('./data/wn-data-eng.tab', 'r')
    wordout = open('word.csv', 'a')

    csvdel = '\t'

    wordout.write('name:string:key' + csvdel + 'synset' + csvdel + 'word\n')

    setVariable()


    for line in omw:
        kv = parseLine(line)
        if not(kv is None):
            linecsv = str(kv[0]) + str(kv[1]) + csvdel +  str(kv[0]) + csvdel + str(kv[1]) +"\n"
            appendLine(wordout, linecsv)

    wordout.close()


if __name__ == "__main__":
    main()
