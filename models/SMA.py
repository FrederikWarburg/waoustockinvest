import numpy as np
from helpers.helpers import get_stock_data, get_plots_path
from helpers.plotter import plot_sma, save_plt, plot_last_x_days
from postprocessing.sendemail import buy, sell

class SMA:
    def __init__(self):
        pass


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
