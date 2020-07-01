import requests
import json
url = "127.0.0.1:8887"
req ={"id":"id0376262",
	"vendor_id":1,
	"pickup_datetime":1467302350000,
	"dropoff_datetime":1467304896000,
	"passenger_count":2,
	"pickup_longitude":-73.873093,
	"pickup_latitude":40.774097,
	"dropoff_longitude":-73.926704,
	"dropoff_latitude":40.856739,
	"store_and_fwd_flag":"N",
	"trip_duration":1}
r = requests.post(url, json=json.dumps(req))
print(r.text)
