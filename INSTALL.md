Setup instructions
==================

Dependencies
------------
omw-graph is (supposedly) tested to work with the following configuration:

* Python 3.3
* Java 1.7
* Neo4j 2.0.1
* batch-importer [2.0 branch] (https://github.com/jexp/batch-import/tree/20)

Batch-importer installation and configuration
---------------------------------------------

Unzip the batch importer zip archive in `omwg/db/neo4j_batch_importer/`.

If you already use the batch importer, add to your `batch.properties` file the following lines:

```
batch_import.node_index.synkey=exact
batch_import.node_index.lexkey=exact
```

Run
---

1. Put your LMF XML files (`*-lmf.xml`) in `omwg/data/`
2. Execute `run.sh`, this will generate:
  * `data/csv-files/word-xxx.csv` (nodes)
  * `data/csv-files/rels-xxx.csv` (edges)
  * `data/csv-files/syn-xxx.csv` (nodes)
  * `data/csv-files/relsynlex-xxx.csv` (edges)
3. The database will be created in `omw-graph/db/`
4. Copy/paste the database in `.../neo4j_folder/data/`
5. Modify neo4j properties to make it use the new db
6. Start/Restart neo4j
