from functions.Helper import *
import pandas as pd
from functions.SMA import *
from functions.plotter import *


def downloadStock(name):
    data = pd.read_csv('{0}/{1}.csv'.format(get_data_path(),name))
    date = data["Date"]
    date_f = []
    for i in range(len(date)):
        date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
    data["Date"] = date_f
    data = data.drop('Unnamed: 6', 1)

    return data

name = "Vertex Pharmaceuticals Incorpo"

stock = downloadStock(name)

price = stock["Close Price"]
date = stock["Date"]

days_since_dc, date_of_dc, short_rolling, long_rolling = days_since_last_deadcross(stock)
days_since_gc, date_of_gc, short_rolling, long_rolling = days_since_last_goldencross(stock)

plt = plot_sma(date, price, short_rolling, long_rolling, days_since_gc, date_of_gc, days_since_dc, date_of_dc)

plt.show()