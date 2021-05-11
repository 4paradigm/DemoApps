#! /bin/sh
#
# init.sh

# clone fedb and sparkfe

# step 1 clone fedb
#git clone https://github.com/4paradigm/fedb.git
#
## step 2 clone hybridse
#git clone https://github.com/4paradigm/HybridSE.git
#
## step 3 download fedb & sparkfe
#wget -O https://github.com/4paradigm/fedb/releases/download/2.2.0/fedb-2.2.0-linux.tar.gz
#tar -zxf fedb-2.2.0-linux.tar.gz
#wget -O https://github.com/4paradigm/SparkFE/releases/download/v0.1.1/spark-3.0.0-bin-sparkfe.tgz
#tar -zxf spark-3.0.0-bin-sparkfe.tgz
#
#yum install java-1.8.0-openjdk-devel
#wget https://archive.apache.org/dist/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz
#tar -zxf zookeeper-3.4.14.tar.gz
#cd $WORKDIR/zookeeper-3.4.14
#
#mv conf/zoo_sample.conf conf/zoo.conf
export JAVA_HOME=/home/jovyan/work/jdk1.8.0_141
export PATH=$JAVA_HOME/bin:$PATH

cd /home/jovyan/work/zookeeper-3.4.14 && ./bin/zkServer.sh start
sleep 1
cd /home/jovyan/work/fedb-2.2.0 && ./bin/start.sh start
sleep 1
cd /home/jovyan/work/fedb-2.2.0 && ./bin/start_ns.sh start
sleep 1
cd /home/jovyan/work/fedb-2.2.0 && ./bin/fedb --interactive=false --zk_cluster=127.0.0.1:2181 --zk_root_path=/fedb --role=sql_client --cmd="show databases;"

