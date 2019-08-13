from helpers.helpers import get_stock_data
import pandas as pd
import os

class Dataset:
    def __init__(self):

        self.data_path = 'data'

    def loadStock(self, name):
        data = pd.read_csv(os.path.join(self.data_path, 'prices', name + '.csv'))
        date = data["Date"]
        date_f = []
        for i in range(len(date)):
            date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
        data["Date"] = date_f
        data = data.drop('Unnamed: 6', 1)

        return data


    def loadStocks(self):
        names, ids = get_stock_data()

        data = {}

        for company in names:
            tmp = pd.read_csv(os.path.join(self.data_path, 'prices', company.replace("/", "") + '.csv'))
            date = tmp["Date"]
            date_f = []
            for i in range(len(date)):
                date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
            tmp["Date"] = date_f
            tmp = tmp.drop('Unnamed: 6', 1)
            data.update({company: tmp})

        return data
