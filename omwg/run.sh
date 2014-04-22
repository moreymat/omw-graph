#!/bin/bash

#--- FUNCTIONS ---#

function usage
{  
  echo "Usage: $0 datadirectory"
}

#
#buildTabFiles
#call all Python scripts in srcs folder
#

function buildCsvFiles
{
  for i in data/wn-*-lmf.xml
  do
      echo -n "Running $i..."
      if ! python3 srcs/lmfparser.py $i ; then
        echo "Error $i"
      else
        echo "[OK]"
      fi
  done
}

#
#getRelsFiles
#fetch all relations filename from a directory
#

function getRelsFiles
{
  for i in data/csv_files/rel-*.csv
  do
    if [ -z "$relsfiles" ];then
      relsfiles=$i
    else
      relsfiles=$relsfiles,$i
    fi
  done
  echo $relsfiles
}

#
#getWordsFiles
#fetch all words filename from a directory
#

function getWordsFiles
{
  for i in data/csv_files/word-*.csv
  do
    if [ -z "$wordfiles" ];then
      wordfiles=$i
    else
      wordfiles=$wordfiles,$i
    fi
  done
  echo $wordfiles
}

#
#quickCleaner
#quick and dirty cleaner just to delete duplicate lines
#

function quickCleaner
{
  echo "quick clean"
  
  for file in data/csv_files/rels-*.csv
  do
    echo "$file"
    { rm $file && sort -u > $file; } < $file
    sed -i 1i"name:string:key\tname:string:key\ttype" $file
  done
  
  for file in data/csv_files/word-*.csv
  do
    echo "$file"
    { rm $file && sort -u > $file; } < $file
    sed -i 1i"name:string:key\tvalue" $file
  done
}

#--- MAIN ---#

# Generate csv files in csv_files folder
buildCsvFiles
#quickCleaner

# target directory
DB="db/omw-graph.db"

# nodes file(s)
NODES=$(getWordsFiles)

# edges file(s)
RELS=$(getRelsFiles)

CP=""
HEAP=4G

# neo4j batch importer 

for i in db/neo4j_batch_importer/lib/*.jar; do CP="$CP":"$i"; done
java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer db/neo4j_batch_importer/batch.properties "$DB" "$NODES" "$RELS" "$@"
