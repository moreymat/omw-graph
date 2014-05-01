#!/usr/bin/env python

from py2neo import neo4j

dburl = 'http://localhost:7474/db/data/'
db = None

def connectDb():
    global dburl
    global db

    db = neo4j.GraphDatabaseService(dburl)

def flateningGraph(nonlex):
    rels = []
    for n in nonlex:
        pwette =  False
        hyporels = n.match_outgoing(rel_type='hypo')
        for h in hyporels:
            pwette = True
            break

        if not pwette:
            if n['name'].split('-')[3] == 'n':
                outrels = list(db.match(start_node=n))
                increls = list(db.match(end_node=n))

                for o in outrels:
                    db.delete(o)
                    print('delelete ' + str(o))


def main():
    global db
    connectDb()

    nonlex = db.find('NonLexicalized')
    flateningGraph(nonlex)



if __name__ == '__main__':
    main()
