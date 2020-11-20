#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

"""

"""

import numpy as np
import tornado.web
import tornado.ioloop
import json
import lightgbm as lgb
import sqlalchemy as db
from sqlalchemy_fedb.fedbapi import Type as feType

bst = lgb.Booster(model_file='model.txt')

engine = db.create_engine('fedb:///db_test?zk=127.0.0.1:2181&zkPath=/fedb', echo=True)
connection = engine.connect()
sql = """select trip_duration, passenger_count,
sum(pickup_latitude) over w as vendor_sum_pl,
max(pickup_latitude) over w as vendor_max_pl,
min(pickup_latitude) over w as vendor_min_pl,
avg(pickup_latitude) over w as vendor_avg_pl,
sum(pickup_latitude) over w2 as pc_sum_pl,
max(pickup_latitude) over w2 as pc_max_pl,
min(pickup_latitude) over w2 as pc_min_pl,
avg(pickup_latitude) over w2 as pc_avg_pl ,
count(vendor_id) over w2 as pc_cnt,
count(vendor_id) over w as vendor_cnt
from t1
window w as (partition by vendor_id order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW),
w2 as (partition by passenger_count order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW);"""

TypeDict = {feType.Bool:"bool", feType.Int16:"smallint", feType.Int32:"int", feType.Int64:"bigint", feType.Float:"float", feType.Double:"double", feType.String:"string", feType.Date:"date", feType.Timestamp:"timestamp"}

table_schema = [
	("id", "string"),
	("vendor_id", "int"),
	("pickup_datetime", "timestamp"),
	("dropoff_datetime", "timestamp"),
	("passenger_count", "int"),
	("pickup_longitude", "double"),
	("pickup_latitude", "double"),
	("dropoff_longitude", "double"),
	("dropoff_latitude", "double"),
	("store_and_fwd_flag", "string"),
	("trip_duration", "int"),
]

def get_schema(conn, sql):
    rs = conn.execute(sql)
    desc = rs._cursor_description()
    cols = list()
    dict_schema = {}
    for i in desc:
        col = i[0]
        col_type = TypeDict[i[1]]
        cols.append((col, col_type))
        dict_schema[col] = col_type
    return cols, dict_schema

sql_schema, dict_schema = get_schema(connection, sql)
json_schema = json.dumps(dict_schema)
def build_feature(rs):
    var_Y = [rs[0]]
    row_X = [rs[1],
            rs[2],
            rs[3],
            rs[4],
            rs[5],
            rs[6],
            rs[7],
            rs[8],
            rs[9],
            rs[10],
            rs[11],
            ]
    var_X = [row_X]
    return np.array(var_X)

class SchemaHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json_schema)

class PredictHandler(tornado.web.RequestHandler):
    def post(self):
        row = json.loads(self.request.body)
        data = list()
        for i in table_schema:
            if i[1] == "string":
                data.append(row.get(i[0], ""))
            elif i[1] == "int32" or i[1] == "double" or i[1] == "timestamp" or i[1] == "bigint":
                data.append(row.get(i[0], 0))
            else:
                data.append(None)
        rs = connection.execute(sql, tuple(data))
        for r in rs:
            ins = build_feature(r)
            self.write("----------------ins---------------\n")
            self.write(str(ins) + "\n")
            duration = bst.predict(ins)
            self.write("---------------predict trip_duration -------------\n")
            self.write("%s s"%str(duration[0]))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("real time execute sparksql demo")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/schema", SchemaHandler),
        (r"/predict", PredictHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8887)
    tornado.ioloop.IOLoop.current().start()
