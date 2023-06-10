from kafka import KafkaConsumer
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn
import pandas as pd
import lightgbm as ltb
import random
from flask import Flask, render_template, request, redirect

consumer = KafkaConsumer('data-stream', bootstrap_servers=['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))

app = Flask(__name__)

@app.route('/get-prediction/', methods=['GET', 'POST'])
def home():
    for message in consumer:
        print("%s key=%s value=%s" % (message.topic, message.key, message.value))
        global lat
        lat = message.value[1]
        global lon
        lon = message.value[2]
        if request.method == 'POST':
            return redirect('/get-prediction2/')
        odp = str(message.value[0])[0:5] + " MJ"
        return render_template('get_prediction.html', message=odp, custom_text = "Naciśnij przycisk żeby przejść na mapę. Nasłonecznienie to: ")

@app.route('/get-prediction2/')
def root():
    markers = [
        {
            'lat': lon,
            'lon': lat,
            'popup': 'Jesteśmy w'
        }
    ]
    return render_template('index.html', markers=markers)


if __name__ == "__main__":
    app.run()
