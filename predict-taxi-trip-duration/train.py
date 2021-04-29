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

from fespark.sql import SparkSession

import numpy as np
import pandas as pd
import lightgbm as lgb

def build_dataset(input_table, sql, tname):
    """
    Process input_table with sql_script and return a dataframe
    """
    spark = SparkSession.builder.appName("fedb demo").getOrCreate()
    df = spark.read.parquet(input_table)
    df.createOrReplaceTempView(tname)
    df_with_sql = spark.sql(sql)
    return df_with_sql.toPandas()

def train(training_df, validating_df):
    """
    Train a model saved as "model.txt" with training_df and validating_df
    """
    y = training_df['trip_duration']
    x = training_df.drop(columns=['trip_duration'])

    y_val = validating_df['trip_duration']
    x_val = validating_df.drop(columns=['trip_duration'])

    lgb_train = lgb.Dataset(x, y)
    lgb_eval = lgb.Dataset(x_val, y_val, reference=lgb_train)
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
    gbm.save_model('model.txt')


with open("./fe.sql", 'r') as fd:
    sql = fd.read()

# build validating and training dataframe
validating_dataset_path = "./data/taxi_tour_table_predict_simple.snappy.parquet"
validating_dataframe = build_dataset(validating_dataset_path, sql, "t1")
training_dataset_path = "./data/taxi_tour_table_train_simple.snappy.parquet"
training_dataframe = build_dataset(training_dataset_path, sql, "t1")

# training 
train(training_dataframe, validating_dataframe)

