import pandas as pd
import os
import datetime


class Dataset:
    def __init__(self, specific_stock = None, start_date = None):

        self.data_path = 'data'
        self.lookup = self.get_stock_lookup(specific_stock)
        self.data = self.loadStocks()
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

    def get_id(self, stock_names):
        if isinstance(stock_names, list):
            pass
        else:
            return self.lookup[self.lookup['instrumentname'] == stock_names]['instrumentid']

    def get_name(self, stock_ids):
        if isinstance(stock_ids, list):
            pass
        else:
            return self.lookup[self.lookup['instrumentid'] == stock_ids]['instrumentname']

    def loadStocks(self):

        data = {}

        for company in self.lookup['instrumentname']:

            tmp = pd.read_csv(os.path.join(self.data_path, 'prices', company.replace("/", "") + '.csv'))
            date = tmp["Date"]
            date_f = []
            for i in range(len(date)):
                date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
            tmp["Date"] = date_f
            tmp = tmp.drop('Unnamed: 6', 1)
            data.update({company: tmp})

        return data

    def get_stock_lookup(self, specific_stock):
        lookup = pd.read_csv(self.data_path + '/stockIDs.csv')
        if specific_stock == None:
            return lookup
        else:
            print(
                lookup
            )
            return lookup[lookup['instrumentname'] == specific_stock]