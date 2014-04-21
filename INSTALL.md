Setup instructions
==================

Dependencies
------------
omw-graph is (supposedly) tested to work with the following configuration:

* Python 3.3
* nltk 3.0a1
* Java 1.7
* Neo4j 2.0.1
* batch-importer [2.0 branch] (https://github.com/jexp/batch-import/tree/20)

Batch-importer installation and configuration
---------------------------------------------

Unzip the batch importer zip archive in `omwg/db/neo4j_batch_importer/`.

If you already use the batch importer, make sure your `batch.properties` file contains this line: `batch_import.node_index.key=exact`.

Run
---

1. Put .xml files in omw-graph/data (english, french, albanese)
2. Launch run.sh script this will generate : 
  * data/tab-files/wn-data-xxx.tab
  * data/csv-files/word-xxx.csv (nodes) 
  * data/csv-files/and rels-xxx.csv (edges)
3. The database will be created in omw-graph/db
4. Copy/paste it in .../neo4j_folder/data
5. Modify neo4j properties to make it use the new db
6. Start/Restart neo4j
