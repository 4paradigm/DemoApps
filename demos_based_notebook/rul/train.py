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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle
import numpy as np
import pandas as pd
import composeml as cp
import utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("sql_file", 
                           help="specify the sql file")
parser.add_argument("model_path",  
                            help="specify the model path")
args = parser.parse_args()
sql_tpl = ""
with open(args.sql_file, "r") as fd:
    sql_tpl = fd.read()

spark = SparkSession.builder.appName("Dataframe demo").getOrCreate()

train_data = utils.load_data('data/train_FD004.txt')

def remaining_useful_life(df):
    return len(df) - 1
lm = cp.LabelMaker(
    target_entity='engine_no',
    time_index='record_time',
    labeling_function=remaining_useful_life,
)
label_times = lm.search(
    train_data.sort_values('record_time'),
    num_examples_per_instance=1,
    minimum_data=100,
    verbose=True,
)
label_times.set_index('engine_no', inplace=True)

# filter train_data
need_drop = []
for idx, row in train_data.iterrows():
    if row['record_time'] > label_times.loc[row['engine_no'],'time']:
        need_drop.append(idx)

filtered = train_data.drop(need_drop)
filtered.sort_values(by='engine_no')

# spark calc
print('spark:')
train_df = spark.createDataFrame(filtered)
train_df.createOrReplaceTempView("rul_table")
fm_res = spark.sql(sql_tpl)
fm = fm_res.toPandas()

fm = fm.groupby(['engine_no']).last().reset_index()
# print(fm)
# add remaining_useful_life col
fm = fm.set_index('engine_no').join(label_times[['remaining_useful_life']])

fm.to_csv('/tmp/train_fm.csv')
print("save the feature matrix done")

fm = pd.read_csv('/tmp/train_fm.csv', index_col='engine_no')
X = fm.copy().fillna(0)
y = X.pop('remaining_useful_life')

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)

# skip baselines

reg = RandomForestRegressor(n_estimators=100)
reg.fit(X_train, y_train)

preds = reg.predict(X_test)
scores = mean_absolute_error(preds, y_test)
print('[Train] Mean Abs Error: {:.2f}'.format(scores))
with open(args.model_path, "wb") as f:
    pickle.dump(reg, f)
