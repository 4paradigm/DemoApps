#! /bin/sh
#
# start_demo.sh

docker run -h=`hostname`  --network=host  4pdosc/openmldb_all_demos:0.3.0 jupyter notebook
