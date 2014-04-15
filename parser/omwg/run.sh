#!/bin/bash

function usage
{
    echo "Usage: $0 datadirectory"
}

function getRelsFiles
{
  for i in csv_files/rels-*.csv
  do
    if [ -z "$relsfiles" ];then
      relsfiles=$i
    else
      relsfiles=$relsfiles,$i
    fi
  done
  echo $relsfiles
}

function getWordsFiles
{
  for i in csv_files/word-*.csv
  do
    if [ -z "$wordfiles" ];then
      wordfiles=$i
    else
      wordfiles=$wordfiles,$i
    fi
  done
  echo $wordfiles
}

DB="db/omw-grap.db"
NODES=$(getWordsFiles)
RELS=$(getRelsFiles)
CP=""
HEAP=4G
for i in db/neo4j_batch_importer/lib/*.jar; do CP="$CP":"$i"; done
#echo java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer batch.properties "$DB" "$NODES" "$RELS" "$@"
java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer db/neo4j_batch_importer/batch.properties "$DB" "$NODES" "$RELS" "$@"
