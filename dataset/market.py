import pandas as pd
import os
import datetime


class MarketDataset:
    def __init__(self, start_date = None):

        self.data_path = 'data'
        self.data = self.loadMarket()
        self.date = pd.to_datetime(start_date, format="%d/%m/%Y")

    def __all__(self):
        return self.data

    def __getitem__(self, date):

        data = {}
        for stock in self.data:
            tmp = self.data[stock][self.data[stock]['Date'] < date]
            if len(tmp) > 0:
                data[stock] = tmp
        return data

    def __next__(self):
        delta = pd.Timedelta(datetime.timedelta(days=1))
        self.date += delta
        return self.__getitem__(self.date)

    def loadMarket(self):

        data = {}

        names = ['S&P', 'c25']

        for company in names:

            tmp = pd.read_csv(os.path.join(self.data_path, 'markets', company.replace("/", "") + '.csv'))
            date = tmp["Date"]
            date_f = []
            for i in range(len(date)):
                date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
            tmp["Date"] = date_f
            tmp = tmp.drop('Unnamed: 6', 1)
            data.update({company: tmp})

        return data