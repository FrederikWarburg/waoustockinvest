import numpy as np
from models.model import Model
from helpers.helpers import get_stock_data, get_plots_path
from helpers.plotter import plot_sma, save_plt, plot_last_x_days
from postprocessing.sendemail import buy, sell
from fbprophet import Prophet

class PROPHET(Model):
    def __init__(self, portefolio):
        super(PROPHET, self).__init__(portefolio)

        self.purchase_ratio = 0.1  # buy for 10 % for a golden cross
        self.purchase_size = self.purchase_ratio * self.portefolio.start_cap
        self.period = 30 # 3 months


    def update(self, data, market_data=None):

        for stock in data:

            prices = data[stock]["Close Price"].values

            df = data[stock]
            df = df.rename(columns={'Date': 'ds', 'Close Price': 'y'})
            df['y'] /= df['y'].values[0]

            m = Prophet(weekly_seasonality=False, yearly_seasonality=False, daily_seasonality=False)
            m.fit(df)

            future = m.make_future_dataframe(periods=self.period)

            forecast = m.predict(future)

            #yhat = (forecast['yhat'].values[-1]  - forecast['yhat'].values[-30])
            #conf_width = (forecast['yhat_upper'].values[-1] - forecast['yhat_lower'].values[-1])
            y_lower = forecast['yhat_lower'].values[-1]

            if y_lower > 1.0:
                amount = int(self.purchase_size / prices[0])

                if amount * prices[0] < self.portefolio.cash and stock not in self.portefolio.deposit:
                    print("purchase ", stock, amount, prices[0])
                    self.portefolio.buy(stock, amount, prices[0])
                else:
                    print("not enought fonds. Optimize prioritazation")

            # dead cross
            if y_lower < 1.0:
                if stock in self.portefolio.deposit:
                    amount = self.portefolio.deposit[stock][0]
                    print("sell ", stock, amount, prices[0])
                    self.portefolio.sell(stock, amount, prices[0])

