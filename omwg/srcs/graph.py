#!/usr/bin/env python

from py2neo import neo4j

dburl = 'http://localhost:7474/db/data/'
db = None

def connectDb():
    global dburl
    global db

    db = neo4j.GraphDatabaseService(dburl)

def flateningGraph(nonlex):
    for n in nonlex:
        hyporels = n.match_incoming(rel_type='hypo')
        for h in hyporels:
            print(h)

def main():
    global db
    connectDb()

    nonlex = db.find('NonLexicalized')
    flateningGraph(nonlex)



if __name__ == '__main__':
    main()
