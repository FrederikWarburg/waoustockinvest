from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd
from helpers.helpers import get_stock_data
import os
import requests

class Scraper:
    def __init__(self):

        self.data_path = 'data'

        if not os.path.isdir(self.data_path + '/descriptions'): os.mkdir(self.data_path + '/descriptions')
        if not os.path.isdir(self.data_path + '/prices'): os.mkdir(self.data_path + '/prices')

    def scrapeStockId(self):

        indexs = ["http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omx-c25"]

        """,      "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omxc-large-cap",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omxc-mid-cap",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omxc-small-cap",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omxc-pi",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omx-c20-cap",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/first-north-all-share-dkk",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/omxn40",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/sverige/omx-stockholm-30",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/sverige/large-cap-pi",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/sverige/mid-cap-pi",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/sverige/small-cap-pi",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/osebx",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/osesx",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/obx",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/oseax",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/osefx",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/norge/oseex",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/tyskland/dax-30",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/tyskland/dax-100",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/tyskland/tecdax",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/tyskland/mdax",
                  "http://www.euroinvestor.dk/markeder/aktier/europa/tyskland/sdax",
                  "http://www.euroinvestor.dk/markeder/aktier/nordamerika/usa/dow-jones",
                  "http://www.euroinvestor.dk/markeder/aktier/nordamerika/usa/nasdaq-100",
                  "http://www.euroinvestor.dk/markeder/aktier/nordamerika/usa/nasdaq-composite",
                  "http://www.euroinvestor.dk/markeder/aktier/nordamerika/usa/sp-500"]"""


        with open('data/stockIDs.csv', 'w') as export:
            export.write('instrumentid,instrumentname\n')

            for index in indexs:
                html = urllib.request.urlopen(index)
                soup = BeautifulSoup(html, "lxml")
                html.close()

                ids = soup.find_all('img', id="imgContextMenu")
                for id in ids:
                    export.write('{1},{0}\n'.format(id['instrumentname'].replace(',',''),id['instrumentid']))

    def scrapeStockTricker(self):

        data = pd.read_csv('data/stockIDs.csv')
        ids = data["instrumentid"]
        names = data["instrumentname"]

        with open('data/Tickers.csv', 'w') as export:
            export.write('instrumentid,instrumentname, Trickers\n')
            i = 0
            for name in names:
                print(name)
                searchname = name.replace("Ø", "o")
                searchname = searchname.lower()
                searchname = searchname.replace("æ", "ae").replace(" b ", " ") \
                    .replace(" a ", " ").replace("a.p.", "ap").replace("å", "aa").replace("a/s b", "a/s") \
                    .replace("ø", "oe").replace("a/s a", "a/s").replace(" ", "+").replace("ó", "o").replace("ö", "o") \
                    .replace("ü", "u").replace("pr&#2", "").replace("+og+", "+&+").replace("ser", "").replace("brdr",
                                                                                                              "broedr") \
                    .replace("sjaelland-fyn+a/s", "sjaelland").replace("plc+a", "plc").replace("capital+a/s+stam",
                                                                                               "capital+a/s") \
                    .replace("dlh+a/s", "dlh").replace("+se", "").replace("+ab+b", "+ab") \
                    .replace("+ab+pref", "+ab").replace("+ab+a", " ab").replace("ab+pr", "ab")

                link = "https://markets.ft.com/data/search?assetClass=Equity&query={}".format(searchname)
                html = urllib.request.urlopen(link)
                soup = BeautifulSoup(html, "lxml")
                html.close()
                ticker = soup.find_all('td', {'class': 'mod-ui-table__cell--text'})
                if len(ticker) > 0:
                    ticker = ticker[1].text
                else:
                    print(name, searchname, ticker)

                export.write('{1},{0},{2}\n'.format(name, ids[i], ticker))
                i = i + 1

    def scrapeStockDescription(self):

        data = pd.read_csv(self.data_path + '/Tickers.csv')
        tickers = data[" Trickers"]

        for ticker in tickers:
            link = "https://markets.ft.com/data/equities/tearsheet/profile?s={}".format(ticker.replace(" ", "%20"))
            html = urllib.request.urlopen(link)
            soup = BeautifulSoup(html, "lxml")
            html.close()
            p = soup.find('p', {'class': 'mod-tearsheet-profile-description mod-tearsheet-profile-section'})
            if p != None:
                with open(self.data_path + '/descriptions/{}.txt'.format(ticker.replace(":", "")),
                          'w') as export:
                    export.write(p.text)
            else:
                with open(self.data_path + '/descriptions/{}.txt'.format(ticker.replace(":", "")),
                          'w') as export:
                    export.write("Sorry - Missing description")
                export.close()
                print("Missing description on {}".format(ticker))

    def scrapeStockPrices(self):
        names, ids = get_stock_data()

        for i in range(0, len(ids)):
            print(i, "/", len(ids))
            link = "http://euroinvestor.com/stock/historicalquotes.aspx?instrumentId={}&amp;format=CSV".format(ids[i])
            r = requests.get(link)
            with open(r"{0}/{1}.csv".format(self.data_path + '/prices', names[i].replace("/", "")), 'wb') as f:
                f.write(r.content)