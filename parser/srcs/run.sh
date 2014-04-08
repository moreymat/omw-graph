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
uniq word.csv > tmp.csv
cat tmp.csv > word.csv
rm tmp.csv

python relationextractor.py "$1"
