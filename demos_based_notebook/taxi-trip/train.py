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

from pyspark.sql import SparkSession
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("sql_file", 
                           help="specify the sql file")
parser.add_argument("model_path",  
                            help="specify the model path")
args = parser.parse_args()

spark = SparkSession.builder.appName("Dataframe demo").getOrCreate()
sql_tpl = ""
with open(args.sql_file, "r") as fd:
    sql_tpl = fd.read()

parquet_predict = "./data/taxi_tour_table_predict_simple.snappy.parquet"
parquet_train = "./data/taxi_tour_table_train_simple.snappy.parquet"
train = spark.read.parquet(parquet_train)
train.createOrReplaceTempView("t1")
train_df = spark.sql(sql_tpl)
train_set = train_df.toPandas()
predict = spark.read.parquet(parquet_predict)
predict.createOrReplaceTempView("t1")
predict_df = spark.sql(sql_tpl)
predict_set = predict_df.toPandas()

y_train = train_set['trip_duration']
x_train = train_set.drop(columns=['trip_duration'])
y_predict = predict_set['trip_duration']
x_predict = predict_set.drop(columns=['trip_duration'])

lgb_train = lgb.Dataset(x_train, y_train)
lgb_eval = lgb.Dataset(x_predict, y_predict, reference=lgb_train)

# specify your configurations as a dict
params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

print('Starting training...')
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

gbm.save_model(args.model_path)
print("save model.txt done")
