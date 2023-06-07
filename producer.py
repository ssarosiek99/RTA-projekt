from kafka import KafkaProducer
from time import sleep
import requests
import pandas as pd
import logging

import json

# Coinbase API endpoint

df = pd.read_json("https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2019-05-17&end_date=2023-05-31&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,sunrise,sunset,shortwave_radiation_sum,rain_sum,windspeed_10m_max,windgusts_10m_max,et0_fao_evapotranspiration&timezone=auto")

df = pd.DataFrame(df['daily'].tolist())

df = df.T

df = df.rename(columns = {0 : "Data", 1 : "temperature_2m_max", 2: "temperature_2m_min", 3 : "temperature_2m_mean", 4 : "sunrise", 5 : "sunset", 6 : "shortwave_radiation_sum", 7 : "rain_sum", 8 : "windspeed_10m_max", 9 : "windgusts_10m_max", 10 : "et0_fao_evapotranspiration"})

    ############### usuwam ostanie dwie obserwacje, jakieś nan tam są
df = df[0:len(df)-2]

X = df.drop(columns = ['shortwave_radiation_sum', 'Data', 'sunrise', 'sunset'])
y = df.shortwave_radiation_sum

# Producing as JSON
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
value_serializer=lambda m: json.dumps(m).encode('ascii'))

while(True):
    sleep(2)
    
    print("Price fetched")
    producer.send('data-stream', X.to_json()).get(timeout=100)
    producer.flush(timeout = 100)

    print("Price sent to consumer")