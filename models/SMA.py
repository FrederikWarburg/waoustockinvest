import numpy as np
from models.model import Model
from helpers.helpers import get_stock_data, get_plots_path
from helpers.plotter import plot_sma, save_plt, plot_last_x_days
from postprocessing.sendemail import buy, sell

class SMA(Model):
    def __init__(self, portefolio):
        super(SMA, self).__init__(portefolio)

        self.purchase_ratio = 0.1 # buy for 10 % for a golden cross
        self.purchase_size = self.purchase_ratio * self.portefolio.start_cap

    def update(self, data, market_data = None):

        for stock in data:

            prices = data[stock]["Close Price"].values

            short_rolling = self.sma(prices, 50)
            long_rolling = self.sma(prices, 200)

            # golden cross
            if long_rolling[1] > short_rolling[1] and long_rolling[0] < short_rolling[0]:
                amount = int(self.purchase_size / prices[0])

                if amount * prices[0] < self.portefolio.cash and stock not in self.portefolio.deposit:
                    print("purchase ", stock, amount, prices[0])

                    self.portefolio.buy(stock, amount, prices[0])

            # dead cross
            if long_rolling[1] < short_rolling[1] and long_rolling[0] >= short_rolling[0]:

                if stock in self.portefolio.deposit:

                    amount = self.portefolio.deposit[stock][0]
                    print("sell ", stock, amount, prices[0])
                    self.portefolio.sell(stock, amount, prices[0])

    def sma(self, price, window):
        if len(price) > window + 1:
            return [np.mean(price[i:i + window]) for i in range(2)]
        else:
            return np.zeros(2)
