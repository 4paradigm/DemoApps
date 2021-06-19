#! /bin/sh
#
# start_predict_server.sh

# "cleanup"
# ps -ef | grep predict_server | grep -v grep | cut -c 9-15 | xargs kill -s 9
echo "start predict server"
nohup python3 predict_server.py $1 $2 $3 >/tmp/p.log 2>&1 &
sleep 1
cat /tmp/p.log

