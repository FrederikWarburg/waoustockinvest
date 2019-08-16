from dataset.dataset import Dataset
from helpers.plotter import plot_sma
from preprocessing.scraper import Scraper
from models.SMA import SMA
from portefolio.portefolio import Portefolio
from models.market import Market
import datetime
from postprocessing.statistics import model_statistics

def main():

    name = None
    start_date = '10/01/2017'

    # download newest data

    scraper = Scraper()
    scraper.scrapeStockLookup()
    scraper.scrapeStockPrices()
    scraper.scrapeMarketPrices()

    return

    # Initialize
    portefolio_baseline = Portefolio()
    portefolio_sma = Portefolio()

    dataset = Dataset(name, start_date)
    model_baseline = Market(portefolio_baseline)
    model_sma = SMA(portefolio_sma)

    while dataset.date < datetime.datetime.today():
        data = dataset.__next__()
        model_baseline.update(data)
        model_sma.update(data)

    print("baseline model")
    model_statistics(portefolio_baseline, dataset)

    print("SMA model")
    model_statistics(portefolio_sma, dataset)

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