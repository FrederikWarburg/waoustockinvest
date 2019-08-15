from dataset.dataset import Dataset
from dataset.market import MarketDataset
from helpers.plotter import plot_sma
from preprocessing.scraper import Scraper
from models.SMA import SMA
from portefolio.portefolio import Portefolio
from models.market import Market
from models.CAPM import CAPM
import datetime
from postprocessing.statistics import model_statistics
import json
import matplotlib.pyplot as plt
import pandas as pd

def main():

    name = None
    start_dates = ['01/01/2016','01/01/2017','01/01/2018','01/01/2019']
    summary_dict = {}

    for start_date in start_dates:

        dataset = Dataset(name, start_date)
        market_dataset = MarketDataset(start_date)

        summary_dict[start_date] = {}

        # Initialize
        #portefolio_baseline = Portefolio()
        #portefolio_sma = Portefolio()
        portefolio_capm = Portefolio()

        #model_baseline = Market(portefolio_baseline)
        #model_sma = SMA(portefolio_sma)
        model_capm = CAPM(portefolio_capm)

        while dataset.date < datetime.datetime.today():
            data = dataset.__next__()
            market_data = market_dataset.__next__()

            #model_baseline.update(data)
            #portefolio_baseline.update(dataset.date, data)

            #model_sma.update(data)
            #portefolio_sma.update(dataset.date, data)

            model_capm.update(data, market_data)
            portefolio_capm.update(dataset.date, data)

        #print("baseline model")
        #value = model_statistics(portefolio_baseline, dataset)
        #summary_dict[start_date]['baseline'] = value
        #plot = portefolio_baseline.plot_internal_val('baseline', 'r')

        #print("SMA model")
        #value = model_statistics(portefolio_sma, dataset)
        #summary_dict[start_date]['SMA'] = value
        #plot = portefolio_sma.plot_internal_val('SMA', 'b')

        print("CAPM model")
        value = model_statistics(portefolio_capm, dataset)
        summary_dict[start_date]['SMA'] = value
        plot = portefolio_capm.plot_internal_val('SMA', 'b')

        #plt.vlines(pd.to_datetime(start_date, format="%d/%m/%Y"), portefolio_baseline.start_cap *0.5, portefolio_baseline.start_cap *1.5)

    plt.legend()
    plt.show()

    print('\n ################ \n SUMMARY \n ################ \n')
    print(json.dumps(summary_dict, indent=4))

if __name__ == '__main__':
    main()