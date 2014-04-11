#!/bin/bash

function usage
{
    echo "Usage: $0 datadirectory"
}

if [ $# -lt 1 ]
then
    usage
    exit -1
fi

python directoryparser.py "$1"
shift

DB="db/omw-grap.db"
NODES="csv_files/eng.csv"
RELS="csv_files/rels-eng.csv"
CP=""
HEAP=4G
for i in db/neo4j_batch_importer/lib/*.jar; do CP="$CP":"$i"; done
#echo java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer batch.properties "$DB" "$NODES" "$RELS" "$@"
java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer db/neo4j_batch_importer/batch.properties "$DB" "$NODES" "$RELS" "$@"
