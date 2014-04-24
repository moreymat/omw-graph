OMW-GRAPH
=========

Data folder
-----------

This folder is used to store files used to populate the db.
OWM-GRAPH will build .csv files from LMF files.

Files produced

* word-xxx.csv - every lexical entry
* syn-xxx.csv  - every synsets entry

each lexical entry is connected to one synset or more

* rel-xxx.csv       - relations between synsets
* relsynlex-xxx.csv - relations between synsets and lexicals entries

.csv files
---------

.csv files are stored in data/csv_files. It is useless once bd is produced.
We will delete them later.
