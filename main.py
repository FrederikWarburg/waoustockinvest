from dataset.dataset import Dataset
from helpers.plotter import plot_sma
from preprocessing.scraper import Scraper
from models.SMA import days_since_last_deadcross, days_since_last_goldencross


def main():

    name = "Ambu AS"

    #scraper = Scraper()
    #scraper.scrapeStockId()
    #scraper.scrapeStockTricker()
    #scraper.scrapeStockDescription()
    #scraper.scrapeStockPrices()

    dataset = Dataset()
    stock = dataset.loadStock(name)

    price = stock["Close Price"]
    date = stock["Date"]

    days_since_dc, date_of_dc, short_rolling, long_rolling = days_since_last_deadcross(stock)
    days_since_gc, date_of_gc, short_rolling, long_rolling = days_since_last_goldencross(stock)

    plt = plot_sma(date, price, short_rolling, long_rolling, days_since_gc, date_of_gc, days_since_dc, date_of_dc)

    plt.show()



    """
    downloadStocks()
    data = loadStocks()
    check_crossovers_c25(data)
    """



#names, ids = get_stock_data()

if __name__ == '__main__':
    main()