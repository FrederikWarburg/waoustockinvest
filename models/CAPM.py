import numpy as np
from loadC25 import *

import scipy.stats as stat

def CAPM(stock):
    # https://www.statistikbanken.dk/statbank5a/SelectVarVal/saveselections.asp
    rf = 0.5

    stock_price = stock["Close Price"]

    market = loadc20()
    market_price = market["Close Price"]

    hist = len(stock_price)
    stock_price_change = calc_day_change(stock_price)
    market_price_change = calc_day_change(market_price[:hist])

    #beta = np.cov(stock_price_change,market_price_change,ddof=0)/np.var(market_price_change)

    s = stat.linregress(market_price_change,stock_price_change)

    rm = np.mean(market_price_change)
    beta = s.slope

    return rf + beta*(rm-rf)


def calc_day_change(stock_price):
    stock_price = np.array(stock_price)
    change = stock_price[1:]/stock_price[:-1]-1
    return change

#downloadc25()
data = loadc25()

for name in h.c25:
#print("so good so fare")
    stock = data[name]
    print(CAPM(stock))


