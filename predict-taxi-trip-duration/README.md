#  Predict Taxi Tour Duration

This demo uses [fedb](https://github.com/4paradigm/fedb) and [SparkFE](https://github.com/4paradigm/NativeSpark) to develop a realtime prediction appliction for the New York City Taxi Trip Duration on [Kaggle](https://www.kaggle.com/c/nyc-taxi-trip-duration/overview)

## Feature Engineering SQL Script

```
sql_tpl = ""select trip_duration, passenger_count,
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
from {}
window w as (partition by vendor_id order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW),
w2 as (partition by passenger_count order by pickup_datetime ROWS_RANGE BETWEEN 1d PRECEDING AND CURRENT ROW)"""
```

## Running the Tour

```
docker run -dt ghcr.io/4paradigm/fedb:2.1.0
# find the container id
CONTAINER_ID=`docker ps | grep fedb | awk '{print $1}'`
docker exec -it ${CONTAINER_ID} /bin/bash
# clone demo apps
git clone https://github.com/4paradigm/DemoApps
# enter the predict-taxi-trip-duration dir
cd DemoApps/predict-taxi-trip-duration
# download nativespark distribution
sh get_deps.sh
# train model
sh train.sh
# import history data to fedb for feature engineering
python3 import.py
# start predict server with model
python3 predict_server.py >log 2>&1 &
# send a http request to predict_server
python3 predict.py
# the output we will see
----------------ins---------------
[[ 2.       40.774097 40.774097 40.774097 40.774097 40.774097 40.774097
  40.774097 40.774097  1.        1.      ]]
---------------predict trip_duration -------------
859.3298781277192 s
```
