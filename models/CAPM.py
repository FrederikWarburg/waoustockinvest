import numpy as np
import scipy.stats as stat

from models.model import Model

class CAPM(Model):
    # Ra = Expected return on a security
    # Rf = Risk-free rate
    # Rm = Return of the market
    # beta = The beta of the security
    # (Rm - Rrf) = Equity market premieum
    def __init__(self, portefolio):
        super(CAPM, self).__init__(portefolio)

        self.rf = 0.05 / 365.0 # 5 % per year risk free
        self.purchase_size = 0.1
        self.period = 10 # months

    def update(self, data, market):

        market_price = market['c25']["Close Price"].values
        market_price_change = self.calc_day_change(market_price)
        rm = np.mean(market_price_change)

        for stock in data:
            prices = data[stock]["Close Price"].values

            stock_price_change = self.calc_day_change(prices)
            model = stat.linregress(market_price_change, stock_price_change)

            beta = model.slope
            ra = self.rf + beta * (rm - self.rf) #linear correlation between risk and return

            if ra > 0.3 / 10.0 :#.03 / 12.0 and ra < 0.50 / 12.0 :# and beta < 1.2: #buy
                amount = int(self.purchase_size / prices[0])

                if amount * prices[0] < self.portefolio.cash and stock not in self.portefolio.deposit:
                    print("purchase ", stock, amount, prices[0])
                    self.portefolio.buy(stock, amount, prices[0])

            else: #sell

                if stock in self.portefolio.deposit:

                    amount = self.portefolio.deposit[stock][0]
                    print("sell ", stock, amount, prices[0])
                    self.portefolio.sell(stock, amount, prices[0])

    def calc_day_change(self, price):
        month_price = np.asarray([np.mean(price[i*30:(i+1)*30]) for i in range(self.period)])
        change = (month_price[:-1] - month_price[1:])/month_price[1:]
        return change


