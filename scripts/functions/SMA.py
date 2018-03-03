import numpy as np
from functions.Helper import *
from functions.sendemail import *
from functions.plotter import *

def sma(price, window):
    if (len(price) - (window - 1)) > 0:
        ma = np.zeros(len(price) - (window - 1))
        for i in range(len(ma)):
            ma[i] = np.mean(price[i:i + window])
        return ma
    else:
        return np.zeros(window)

def days_since_last_goldencross(stock):
    price = stock["Close Price"]
    date = stock["Date"]

    short_rolling = sma(price, 50)
    long_rolling = sma(price, 200)

    if long_rolling.all() != 0:
        for i in range(len(long_rolling) - 1):
            # golden cross
            if long_rolling[i + 1] > short_rolling[i + 1] and long_rolling[i] <= short_rolling[i]:
                return i, date.dt.date.values[i], short_rolling, long_rolling

    return -1, -1, short_rolling, long_rolling


def days_since_last_deadcross(stock):
    price = stock["Close Price"]
    date = stock["Date"]

    short_rolling = sma(price, 50)
    long_rolling = sma(price, 200)

    if long_rolling.all() != 0:
        for i in range(len(long_rolling) - 1):
            # dead cross
            if long_rolling[i + 1] < short_rolling[i + 1] and long_rolling[i] >= short_rolling[i]:
                return i, date.dt.date.values[i], short_rolling, long_rolling
    return -1, -1, short_rolling, long_rolling


def check_crossovers_c25(data):
    names, ids = get_stock_data()
    for stock_name in names:
        stock = data[stock_name]
        print(stock_name)
        days_since_dc, date_of_dc, short_rolling, long_rolling = days_since_last_deadcross(stock)
        days_since_gc, date_of_gc, short_rolling, long_rolling = days_since_last_goldencross(stock)
        # test what happens with weekends??
        if days_since_dc == 1:

            plt = plot_sma(stock["Date"],stock["Close Price"],
                             short_rolling,long_rolling,
                             days_since_gc,date_of_gc,
                             days_since_dc,date_of_dc)

            save_plt(plt, "{0}/deadcross{1}.png".format(get_plots_path(), stock_name.replace("/","")))

            sell(stock_name, date)

        if days_since_gc == 1:

            plt = plot_sma(stock["Date"], stock["Close Price"],
                             short_rolling, long_rolling,
                             days_since_gc, date_of_gc,
                             days_since_dc, date_of_dc)

            save_plt(plt,
                       "{0}/goldencross{1}.png".format(get_plots_path(),stock_name.replace("/","")))

            buy(stock_name, date)
