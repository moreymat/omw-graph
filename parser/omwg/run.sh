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
