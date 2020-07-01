#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

"""

"""

import numpy as np
import tornado.web
import tornado.ioloop
from fedb import driver
import json
import lightgbm as lgb
bst = lgb.Booster(model_file='model.txt')

options = driver.DriverOptions("127.0.0.1:2181", "/fedb")
fedb_driver = driver.Driver(options)
if not fedb_driver.init():
    sys.exit(-1)
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

def build_feature(rs):
    var_Y = [rs.GetInt32Unsafe(0)]
    row_X = [rs.GetInt32Unsafe(1), 
            rs.GetDoubleUnsafe(2),
            rs.GetDoubleUnsafe(3),
            rs.GetDoubleUnsafe(4),
            rs.GetDoubleUnsafe(5),
            rs.GetDoubleUnsafe(6),
            rs.GetDoubleUnsafe(7),
            rs.GetDoubleUnsafe(8),
            rs.GetDoubleUnsafe(9),
            rs.GetInt32Unsafe(10),
            rs.GetInt32Unsafe(11),
            ]
    var_X = [row_X]
    return np.array(var_X)

class SchemaHandler(tornado.web.RequestHandler):
    def get(self):
        ok, req = fedb_driver.getRequestBuilder('db_demo', sql)
        if not ok or not req:
            self.write("fail to get req")
        input_schema = req.GetSchema()
        if not input_schema:
            self.write("no schema found")
        schema = {}
        for i in range(input_schema.GetColumnCnt()):
            schema[input_schema.GetColumnName(i)] = input_schema.GetColumnTypeName(i)
        self.write(json.dumps(schema))

class PredictHandler(tornado.web.RequestHandler):
    def post(self):
        row = json.loads(self.request.body)
        ok, req = fedb_driver.getRequestBuilder('db_demo', sql)
        if not ok or not req:
            self.write("fail to get req")
            return
        input_schema = req.GetSchema()
        if not input_schema:
            self.write("no schema found")
            return
        str_length = 0
        for i in range(input_schema.GetColumnCnt()):
            print(input_schema.GetColumnTypeName(i))
            if input_schema.GetColumnTypeName(i) == 'string':
                print("str col %s"%row.get(input_schema.GetColumnName(i), ''))
                str_length = str_length + len(row.get(input_schema.GetColumnName(i), ''))
        print("str_length %d"%str_length)
        req.Init(str_length)
        for i in range(input_schema.GetColumnCnt()):
            if input_schema.GetColumnTypeName(i) == 'string':
                req.AppendString(row.get(input_schema.GetColumnName(i), ''))
            elif input_schema.GetColumnTypeName(i) == 'int32':
                req.AppendInt32(int(row.get(input_schema.GetColumnName(i), 0)))
            elif input_schema.GetColumnTypeName(i) == 'double':
                req.AppendDouble(float(row.get(input_schema.GetColumnName(i), 0)))
            elif input_schema.GetColumnTypeName(i) == 'timestamp':
                req.AppendTimestamp(int(row.get(input_schema.GetColumnName(i), 0)))
            else:
                req.AppendNULL()
        if not req.Build():
            self.write("fail to build request")
            return

        ok, rs = fedb_driver.executeQuery('db_demo', sql, req)
        if not ok:
            self.write("fail to execute sql")
            return
        rs.Next()
        ins = build_feature(rs)
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
