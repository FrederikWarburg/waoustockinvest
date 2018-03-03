from functions.Helper import *
import pandas as pd
import requests

def downloadStocks():
    names, ids = get_stock_data()

    for i in range(0,len(ids)):
        print(i)
        link = "http://euroinvestor.com/stock/historicalquotes.aspx?instrumentId={}&amp;format=CSV".format(ids[i])
        r = requests.get(link)
        with open(r"{0}/{1}.csv".format(get_data_path(), names[i].replace("/","")), 'wb') as f:
            f.write(r.content)

def loadStocks():
    names, ids = get_stock_data()

    data = {}

    for company in names:
        tmp = pd.read_csv(r"{0}/{1}.csv".format(get_data_path(), company.replace("/","")))
        date = tmp["Date"]
        date_f = []
        for i in range(len(date)):
            date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
        tmp["Date"] = date_f
        tmp = tmp.drop('Unnamed: 6', 1)
        data.update({company: tmp})

    return data
