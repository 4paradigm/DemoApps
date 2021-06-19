#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2021 4Paradigm
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
"""
import sqlalchemy as db


import sys
import datetime

ddl="""
create table rul_table(
engine_no int,
time_in_cycles int,
operational_setting_1 double,
operational_setting_2 double,
operational_setting_3 double,
sensor_measurement_1 double,
sensor_measurement_2 double,
sensor_measurement_3 double,
sensor_measurement_4 double,
sensor_measurement_5 double,
sensor_measurement_6 double,
sensor_measurement_7 double,
sensor_measurement_8 double,
sensor_measurement_9 double,
sensor_measurement_10 double,
sensor_measurement_11 double,
sensor_measurement_12 double,
sensor_measurement_13 double,
sensor_measurement_14 double,
sensor_measurement_15 double,
sensor_measurement_16 double,
sensor_measurement_17 double,
sensor_measurement_18 double,
sensor_measurement_19 double,
sensor_measurement_20 double,
sensor_measurement_21 double,
record_index int,
record_time timestamp,
index(key=engine_no, ts=record_time),
index(key=time_in_cycles, ts=record_time)
);
"""
engine = db.create_engine('fedb:///db_test?zk=127.0.0.1:2181&zkPath=/fedb')
connection = engine.connect()
try:
    connection.execute("create database db_test;");   
except Exception as e:
    print(e)
try:
    connection.execute("drop table rul_table;");
except Exception as e:
    print(e)

try:
    connection.execute(ddl);
except Exception as e:
    print(e)

def insert_row(row):
#     print(int(row[-1].timestamp())*1000, int(datetime.datetime.strptime(row[-1].strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').timestamp() * 1000))
    row[-1] = int(row[-1].timestamp())*1000
    insert = "insert into rul_table values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"% tuple(row)
    connection.execute(insert)

import utils
data = utils.load_data('data/test_FD004.txt')

for idx, row in data.iterrows():
    if idx > 100:
        break
    insert_row(row)

result = connection.execute("select * from rul_table limit 5;");
print("peek rul_table:")
for r in result:
    print(r)
