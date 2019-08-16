import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Portefolio:
    def __init__(self):
        self.start_cap = 1000000.0
        self.cash = self.start_cap
        self.deposit = {}
        self.trade_cost = 29.0
        self.internal_value = pd.DataFrame(columns = ['data', 'value'])
        self.trades = 0

    def get_value(self, data):

        value = self.cash
        for stock in self.deposit:
            amount, purchase_price = self.deposit[stock]
            current_price = data[stock]['Close Price'].values[0]
            value += current_price * amount

        return value

    def get_deposit(self):
        return self.deposit

    def update(self, date, data):

        value = self.get_value(data)
        self.internal_value = self.internal_value.append(pd.DataFrame(np.asarray([[date, value]]), columns = ['date','value']))

    def get_stock(self, name):

        if name in self.deposit:
            return self.deposit[name]
        else:
            print('not in you deposit')

    def buy(self, name, amount, price):

        if self.cash > amount * price + self.trade_cost:
            if name in self.deposit:
                self.deposit[name] = (self.deposit[name][0] + amount, 1.0 / self.deposit[name][0] + amount * (self.deposit[name][0]*self.deposit[name][1] + amount*price))
            else:
                self.deposit[name] = (amount, price)
            self.cash -= amount*price + self.trade_cost
            self.trades += 1

        else:
            print('Not enough cash')

    def sell(self, name, amount, price):

        if name not in self.deposit: print("You don't own that stock")

        if self.deposit[name][0] == amount:
            del self.deposit[name]
            self.cash += amount * price - self.trade_cost
            self.trades += 1
        elif amount < self.deposit[name][0]:
            self.deposit[name][0] -= amount
            self.cash += amount * price - self.trade_cost
            self.trades += 1
        else:
            print('You do not own that many')

    def plot_internal_val(self, label, col):
        line_types = ['-','--','-.']
        colors = ['r','b','g','k','c','y']
        return plt.plot(self.internal_value['date'], self.internal_value['value'], line_types[np.random.randint(len(line_types))], color = colors[col%len(colors)], label=label )







