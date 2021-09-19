import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.vector_ar.var_model import VAR
from random import random
import requests
import time
import os

a = []
with open("data.txt", 'r') as file:
    while file.readline():
        a.append(file.readline()[:-1].split())

for line in range(len(a)):
    for number in range(len(a[line])):
        a[line][number] = float(a[line][number])

column_names = [
    'altimeter_type',
    'cycle',
    'year',
    'observation_count',
    'observation_count_weighted',
    'gmsl_variation',
    'gmsl_variation_std',
    'gmsl_variation_smooth',
    'gmsl_variation_with_gia',
    'gmsl_variation_with_gia_std',
    'gmsl_variation_with_gia_smooth',
    'gmsl_variation_with_gia_smooth_and_signals_removed',
]
df = pd.DataFrame(a, columns = column_names)

df["gmsl_variation_with_gia_smooth_and_signals_removed"] = df["gmsl_variation_with_gia_smooth_and_signals_removed"] + abs(min(df["gmsl_variation_with_gia_smooth_and_signals_removed"]))

def elevation(lat, long):
    r = requests.get('https://api.open-elevation.com/api/v1/lookup?locations=' + str(lat) + "," + str(long))
    elevation = r.json()["results"][0]["elevation"]
    print(elevation)
def empty_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if filename[0] == "0":
            os.remove(file_path)
def coordinates(lat, long):
    r = requests.get('https://api.open-elevation.com/api/v1/lookup?locations=' + str(lat) + "," + str(long))
    elevation = r.json()["results"][0]["elevation"]
    model = VAR(df[['year','gmsl_variation_with_gia_smooth_and_signals_removed']])
    model_fit = model.fit()
    yhat = model_fit.forecast(model_fit.y, steps=1)
    data = df[['year','gmsl_variation_with_gia_smooth_and_signals_removed']]
    predicted = data.append(pd.DataFrame(yhat, columns=data.columns), ignore_index=True)
    if elevation > 10:
        return "More than 100 years", "images/base.png"
    while yhat[0][1] < elevation * 100:
        model = VAR(predicted[['year','gmsl_variation_with_gia_smooth_and_signals_removed']])
        model_fit = model.fit()
        yhat = model_fit.forecast(model_fit.y, steps=1)
        num = 2.3
        if random() > 0.5: num = -2
        yhat[0][1] += num * random()
        data = predicted[['year','gmsl_variation_with_gia_smooth_and_signals_removed']]
        predicted = data.append(pd.DataFrame(yhat, columns=data.columns), ignore_index=True)
    predicted["gmsl_variation_with_gia_smooth_and_signals_removed"] = predicted["gmsl_variation_with_gia_smooth_and_signals_removed"] + abs(min(predicted["gmsl_variation_with_gia_smooth_and_signals_removed"]))
    fig = predicted.plot(x='year', y='gmsl_variation_with_gia_smooth_and_signals_removed',figsize=(7, 4), zorder=2)
    fig.set_ylabel("elevation of sea in cm")
    fig.legend("")
    name = "images/" + str(random()) + ".png"
    empty_directory("images")
    fig.figure.savefig(name)
    plt.cla()
    plt.close()
    time.sleep(1)
    return (int(str(predicted["year"][len(predicted) - 1]).split(".")[0])) - 2021, name
