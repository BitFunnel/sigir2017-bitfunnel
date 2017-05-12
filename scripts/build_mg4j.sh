#!/bin/bash
set -e

MG4JCLASSPATH = /mnt/d/git/mg4j-workbench/target/mg4j-1.0-SNAPSHOT.jar
INDEXES = /mnt/d/temp/testindexes
BASENAME = 273-1024-2047

MG4JINDEX = $INDEXES/$BASENAME/mg4j
MANIFEST = $MG4JINDEX/$BASENAME-manifest.txt

starttime=$(date +%s)

pushd $MG4JINDEX

split -n l/16 $MANIFEST split-

(for split in split-*; do
(
    ls -l $split
)& 

done

wait)

popd

endtime=$(date +%s)

echo "Indexing time: $((endtime-starttime))s"
