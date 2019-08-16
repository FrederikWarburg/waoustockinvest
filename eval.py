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
from models.modelInit import modelInitializer

def main():

    name = None
    start_dates = ['01/01/2016','01/01/2017','01/01/2018','01/01/2019']
    models = ['MARKET','SMA','CAPM']
    summary_dict = {}
    model_dict = {}

    for start_date in start_dates:

        dataset = Dataset(name, start_date)
        market_dataset = MarketDataset(start_date)

        summary_dict[start_date], model_dict[start_date] = {}, {}

        # Initialize
        for model in models:
            model_dict[start_date][model] = {}

            model_dict[start_date][model]['portefolio'] = Portefolio()
            model_dict[start_date][model]['model'] = modelInitializer(model, model_dict[start_date][model]['portefolio'])

        while dataset.date < datetime.datetime.today():
            data = dataset.__next__()
            market_data = market_dataset.__next__()

            for model in models:
                model_dict[start_date][model]['model'].update(data, market_data)
                model_dict[start_date][model]['portefolio'].update(dataset.date, data)

        for i, model in enumerate(models):
            print(model)
            value = model_statistics(model_dict[start_date][model]['portefolio'], dataset)
            summary_dict[start_date][model] = value
            plot = model_dict[start_date][model]['portefolio'].plot_internal_val(model, i)

            if i == len(models):
                plt.vlines(pd.to_datetime(start_date, format="%d/%m/%Y"), [start_date][model]['portefolio'].start_cap *0.5, [start_date][model]['portefolio'].start_cap *1.5)

    plt.legend()
    plt.show()

    print('\n ################ \n SUMMARY \n ################ \n')
    print(json.dumps(summary_dict, indent=4))

if __name__ == '__main__':
    main()