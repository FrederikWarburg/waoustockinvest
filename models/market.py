from models.model import Model

class Market(Model):
    def __init__(self, portefolio):
        super(Market, self).__init__(portefolio)
        self.day = 0

    def update(self, data, market_data = None):
        if self.day == 0:
            cash = self.portefolio.cash
            stocks = float(len(data))

            price = cash/stocks - stocks*self.portefolio.trade_cost
            for stock in data:
                amount = int(price / data[stock]['Close Price'].values[0])
                self.portefolio.buy(stock, amount, data[stock]['Close Price'].values[0])

        self.day += 1
