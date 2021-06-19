#! /bin/sh
#
# init.sh

export JAVA_HOME=/home/jovyan/work/system/jdk1.8.0_141
export PATH=$JAVA_HOME/bin:$PATH

cd /home/jovyan/work/system/fedb-2.2.0 && ./bin/fedb --interactive=false --zk_cluster=127.0.0.1:2181 --zk_root_path=/fedb --role=sql_client --cmd="show databases;"
if [ $? -eq 0 ]
then
    echo "OpenMLDB has been started"
else
    cd /home/jovyan/work/system/zookeeper-3.4.14 && ./bin/zkServer.sh start
    sleep 1
    cd /home/jovyan/work/system/fedb-2.2.0 && ./bin/start.sh start
    sleep 1
    cd /home/jovyan/work/system/fedb-2.2.0 && ./bin/start_ns.sh start
    sleep 1
fi
