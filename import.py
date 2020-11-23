#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
"""
import sqlalchemy as db


import sys
import datetime

ddl="""
create table t1(
id string,
vendor_id int,
pickup_datetime timestamp,
dropoff_datetime timestamp,
passenger_count int,
pickup_longitude double,
pickup_latitude double,
dropoff_longitude double,
dropoff_latitude double,
store_and_fwd_flag string,
trip_duration int,
index(key=vendor_id, ts=pickup_datetime),
index(key=passenger_count, ts=pickup_datetime)
);
"""
engine = db.create_engine('fedb:///db_test?zk=127.0.0.1:2181&zkPath=/fedb')
connection = engine.connect()
try:
    connection.execute("create database db_test;");
except Exception as e:
    print(e)
try:
    connection.execute(ddl);
except Exception as e:
    print(e)

def insert_row(line):
    row = line.split(',')
    row[2] = '%dl'%int(datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    row[3] = '%dl'%int(datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    insert = "insert into t1 values('%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s);"% tuple(row)
    connection.execute(insert)

with open('data/taxi_tour_table_train_simple.csv', 'r') as fd:
    idx = 0
    for line in fd:
        if idx == 0:
            idx = idx + 1
            continue
        insert_row(line.replace('\n', ''))
        idx = idx + 1
