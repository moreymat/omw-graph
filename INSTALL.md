OMW-GRAPH
=========

Welcome to Open Multilanguage Wordnet (OMW-GRAPH)

Prerequisites
-------------

* Python 3.3
* Java 1.7
* Neo4j 2.0.1
* batch-importer 2.0 branch https://github.com/jexp/batch-import/tree/20

Batch-importer installation and configuration
---------------------------------------------

Unzip batch-importer in omw-graph folder.

You have to configure the batch importer.

* if you have already use it add this line to the batch.properties file:
  batch_import.node_index.synkey=exact
  batch_import.node_index.lexkey=exact

* or just use the batch.properties we created for you in:
  omw-graph/doc/conf

Run
---

1. Put *-lmf.xml files in omw-graph/data
2. Launch run.sh script this will generate : 
  * data/csv-files/word-xxx.csv (nodes) 
  * data/csv-files/rels-xxx.csv (edges)
  * data/csv-files/syn-xxx.csv (nodes)
  * data/csv-files/relsynlex-xxx.csv (edges)
3. The database will be created in omw-graph/db
4. Copy/paste it in .../neo4j_folder/data
5. Modify neo4j properties to make it use the new db
6. Start/Restart neo4j
