from dataset.dataset import Dataset
from helpers.plotter import plot_sma
from preprocessing.scraper import Scraper
from models.SMA import days_since_last_deadcross, days_since_last_goldencross
from portefolio.portefolio import Portefolio
from models.market import Market
import datetime

def main():

    name = "Ambu A/S"
    start_date = '10/01/2016'

    # download newest data

    #scraper = Scraper()
    #scraper.scrapeStockId()
    #scraper.scrapeStockTricker()
    #scraper.scrapeStockDescription()
    #scraper.scrapeStockPrices()

    # Initialize
    portefolio = Portefolio()
    dataset = Dataset(name, start_date)
    model = Market(portefolio)

    while dataset.date < datetime.datetime.today():
        data = dataset.__next__()
        model.update(data)

    print("success!")
    print(portefolio.get_value(dataset.__all__()))

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