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

import requests
import os
import base64
import random
import time
import hashlib

url = "http://127.0.0.1:9887/predict"
req ={
"engine_no":1,
"time_in_cycles":50,
"operational_setting_1" : 35.0033,
"operational_setting_2" : 0.84,
"operational_setting_3" : 100.0,
"sensor_measurement_1" : 449.44,
"sensor_measurement_2" : 0,
"sensor_measurement_3" : 0,
"sensor_measurement_4" : 0,
"sensor_measurement_5" : 0,
"sensor_measurement_6" : 0,
"sensor_measurement_7" : 0,
"sensor_measurement_8" : 0,
"sensor_measurement_9" : 0,
"sensor_measurement_10" : 0,
"sensor_measurement_11" : 0,
"sensor_measurement_12" : 0,
"sensor_measurement_13" : 0,
"sensor_measurement_14" : 0,
"sensor_measurement_15" : 0,
"sensor_measurement_16" : 0,
"sensor_measurement_17" : 0,
"sensor_measurement_18" : 0,
"sensor_measurement_19" : 0,
"sensor_measurement_20" : 0,
"sensor_measurement_21" : 0,
"record_index": 1,
"record_time": 976744800000,
}
r = requests.post(url, json=req)
print(r.text)
print("Congraduation! You have finished the task.")
tmp = os.urandom(44)
secret_key = base64.b64encode(tmp)
print("Your Key:" + str(secret_key))

