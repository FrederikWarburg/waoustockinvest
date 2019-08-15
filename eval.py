from dataset.dataset import Dataset
from helpers.plotter import plot_sma
from preprocessing.scraper import Scraper
from models.SMA import SMA
from portefolio.portefolio import Portefolio
from models.market import Market
import datetime
from postprocessing.statistics import model_statistics
import json
import matplotlib.pyplot as plt
import pandas as pd

def main():

    name = None
    start_dates = ['01/01/2016','01/01/2017','01/01/2018','01/01/2019']
    summary_dict = {}

    # download newest data

    #scraper = Scraper()
    #scraper.scrapeStockId()
    #scraper.scrapeStockTricker()
    #scraper.scrapeStockDescription()
    #scraper.scrapeStockPrices()



    for start_date in start_dates:

        dataset = Dataset(name, start_date)

        summary_dict[start_date] = {}

        # Initialize
        portefolio_baseline = Portefolio()
        portefolio_sma = Portefolio()

        model_baseline = Market(portefolio_baseline)
        model_sma = SMA(portefolio_sma)

        while dataset.date < datetime.datetime.today():
            data = dataset.__next__()
            model_baseline.update(data)
            portefolio_baseline.update(dataset.date, data)

            model_sma.update(data)
            portefolio_sma.update(dataset.date, data)

        print("baseline model")
        value = model_statistics(portefolio_baseline, dataset)
        summary_dict[start_date]['baseline'] = value
        plot = portefolio_baseline.plot_internal_val('baseline', 'r')

        print("SMA model")
        value = model_statistics(portefolio_sma, dataset)
        summary_dict[start_date]['SMA'] = value
        plot = portefolio_sma.plot_internal_val('SMA', 'b')

        plt.vlines(pd.to_datetime(start_date, format="%d/%m/%Y"), portefolio_baseline.start_cap *0.5, portefolio_baseline.start_cap *1.5)

    plt.legend()
    plt.show()

    print('\n ################ \n SUMMARY \n ################ \n')
    print(json.dumps(summary_dict, indent=4))
    """
    stock = dataset.__all__()
    stock = stock[name]

    price = stock["Close Price"]
    date = stock["Date"]

    days_since_dc, date_of_dc, short_rolling, long_rolling = days_since_last_deadcross(stock)
    days_since_gc, date_of_gc, short_rolling, long_rolling = days_since_last_goldencross(stock)

    plt = plot_sma(date, price, short_rolling, long_rolling, days_since_gc, date_of_gc, days_since_dc, date_of_dc)

    plt.show()
    """

#names, ids = get_stock_data()

if __name__ == '__main__':
    main()