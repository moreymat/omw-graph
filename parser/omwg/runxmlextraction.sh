#! /bin/bash

for i in srcs/*2tab.py
do
    echo -n "Running $i..."
    python3 $i
    echo "[OK]"
done
