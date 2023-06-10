from kafka import KafkaConsumer
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn
import pandas as pd
import lightgbm as ltb
import random
from flask import Flask, render_template, request

# # Getting the data as JSON
consumer = KafkaConsumer('data-stream',
bootstrap_servers=['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('ascii')))


app = Flask(__name__)



@app.route('/get-prediction/')
def home():
    for message in consumer:
        print("%s key=%s value=%s" % (message.topic, message.key, message.value))
        global lat
        lat = message.value[1]
        global len
        len = message.value[2]
        return(str((message.value[0])))

@app.route('/get-prediction2/')
def root():
    markers=[
        {
        'lat': len,
        'lon': lat,
        'popup':'Jestesmy w'  
        }
    ]
    return render_template('index.html',markers=markers )


if __name__ == "__main__":
    app.run()

