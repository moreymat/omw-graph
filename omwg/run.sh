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

function getRels
{
  for i in data/csv_files/rel-*.csv
  do
    if [ -z "$relsfiles" ];then
      relsfiles=$i
    else
      relsfiles=$relsfiles,$i
    fi
  done
  
  for i in data/csv_files/relsynlex-*.csv
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

function getNodes
{
  for i in data/csv_files/word-*.csv
  do
    if [ -z "$wordfiles" ];then
      wordfiles=$i
    else
      wordfiles=$wordfiles,$i
    fi
  done

  for i in data/csv_files/syn-*.csv
  do
    if [ -z "$wordfiles" ];then
      wordfiles=$i
    else
      wordfiles=$wordfiles,$i
    fi
  done

  echo $wordfiles
}

#--- MAIN ---#

# Generate csv files in csv_files folder
buildCsvFiles

# target directory
DB="db/omw-graph.db"

# nodes file(s)
NODES=$(getNodes)

# edges file(s)
RELS=$(getRels)

CP=""
HEAP=4G

# neo4j batch importer 

for i in db/neo4j_batch_importer/lib/*.jar; do CP="$CP":"$i"; done
java -classpath $CP -Xmx$HEAP -Xms$HEAP -Dfile.encoding=UTF-8 org.neo4j.batchimport.Importer db/neo4j_batch_importer/batch.properties "$DB" "$NODES" "$RELS" "$@"
