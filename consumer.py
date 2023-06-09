from kafka import KafkaConsumer
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn
import pandas as pd
import lightgbm as ltb
import random
from flask import Flask

# # Getting the data as JSON
consumer = KafkaConsumer('data-stream',
bootstrap_servers=['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('ascii')))


df = pd.read_json("https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2019-05-17&end_date=2023-05-31&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,sunrise,sunset,shortwave_radiation_sum,rain_sum,windspeed_10m_max,windgusts_10m_max,et0_fao_evapotranspiration&timezone=auto")

df = pd.DataFrame(df['daily'].tolist())

df = df.T

df = df.rename(columns = {0 : "Data", 1 : "temperature_2m_max", 2: "temperature_2m_min", 3 : "temperature_2m_mean", 4 : "sunrise", 5 : "sunset", 6 : "shortwave_radiation_sum", 7 : "rain_sum", 8 : "windspeed_10m_max", 9 : "windgusts_10m_max", 10 : "et0_fao_evapotranspiration"})

    ############### usuwam ostanie dwie obserwacje, jakieś nan tam są
df = df[0:len(df)-2]

X = df.drop(columns = ['shortwave_radiation_sum', 'Data', 'sunrise', 'sunset'])
y = df.shortwave_radiation_sum

for col in X.columns:
        X[col] = X[col].astype('float')

X = X.astype(float)
y = y.astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)


model = ltb.LGBMRegressor()
model.fit(X_train, y_train)

app = Flask(__name__)

@app.route('/get-prediction/')
def home():
    for message in consumer:

        df2 = pd.read_json(message.value)
        ran = random.randint(1, 50)
        predicted_y = model.predict(df2.values[:ran])
        print(df2.values[:ran][0][1])

        if predicted_y[0] > 20:
             decision = " Nie wychodz z domu /n"
        else:
             decision = " Mozna wyjsc z domu"

        return "Na podstawie modelu promieniowanie sloneczne krtokofalowe wyniesie " + str(predicted_y[0]) + " \n" + decision + "\n Wyboru dokonano na podstawie danych temperature_2m_max {}, temperature_2m_min {}, temperature_2m_mean {}, rain_sum {}, windspeed_10m_max {}, windgusts_10m_max  {}, et0_fao_evapotranspiration {}   ".format(df2.values[:ran][0][0],df2.values[:ran][0][1], df2.values[:ran][0][2] ,df2.values[:ran][0][3] ,df2.values[:ran][0][4],df2.values[:ran][0][5],df2.values[:ran][0][6]) 




if __name__ == "__main__":
    app.run()

