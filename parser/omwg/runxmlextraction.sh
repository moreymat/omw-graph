#! /bin/bash

function run
{
    echo -n "Running $1..."
    python3 $1
    echo "[OK]"
}

for i in *
do
    if [ $i == 'als2tab.py' ]
    then
        run $i
    fi
    if [ $i == 'fra2tab.py' ]
    then
        run $i
    fi
done
