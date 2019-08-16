from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd
import os
import requests

class Scraper:
    def __init__(self):

        self.data_path = 'data'

        if not os.path.isdir(self.data_path + '/stocks'): os.mkdir(self.data_path + '/stocks')
        if not os.path.isdir(self.data_path + '/markets'): os.mkdir(self.data_path + '/markets')

    def scrapeStockLookup(self):

        data = self.scrapeStockIds()
        data = self.scrapeStockTickers(data)
        data = self.scrapeStockDescriptions(data)

        data.to_csv(os.path.join(self.data_path, 'lookup.csv'), sep = ';')

    def scrapeStockIds(self):

        data = pd.DataFrame(columns=['instrumentid', 'instrumentname'])

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


        for index in indexs:
            html = urllib.request.urlopen(index)
            soup = BeautifulSoup(html, "lxml")
            html.close()

            ids = soup.find_all('img', id="imgContextMenu")
            for id in ids:
                data = data.append(pd.DataFrame([[id['instrumentname'].replace(',',''),id['instrumentid']]], columns = ['instrumentname','instrumentid']))

        return data.reset_index(drop=True)

    def scrapeStockTickers(self, data):

        tickers = []
        for i, name in enumerate(data["instrumentname"]):
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
                print("ERROR with TICKER", name, searchname, ticker)
                ticker = ''

            tickers.append(ticker)

        data['ticker'] = tickers

        return data

    def scrapeStockDescriptions(self, data):

        descriptions = []

        for ticker in data["ticker"]:
            link = "https://markets.ft.com/data/equities/tearsheet/profile?s={}".format(ticker.replace(" ", "%20"))
            html = urllib.request.urlopen(link)
            soup = BeautifulSoup(html, "lxml")
            html.close()
            p = soup.find('p', {'class': 'mod-tearsheet-profile-description mod-tearsheet-profile-section'})
            if p != None:
                descriptions.append(p.text.replace(';','.'))
            else:
                descriptions.append("Sorry - Missing description")
                print("Missing description on {}".format(ticker))

        data['description'] = descriptions

        return data

    def scrapeStockPrices(self):
        lookup = pd.read_csv(os.path.join(self.data_path,'lookup.csv'),sep = ';')

        for i, id in enumerate(lookup['instrumentid']):
            print(i, "/", len(lookup['instrumentid']))
            link = "http://euroinvestor.com/stock/historicalquotes.aspx?instrumentId={}&amp;format=CSV".format(id)
            r = requests.get(link)
            with open(r"{0}/{1}.csv".format(self.data_path + '/stocks', id), 'wb') as f:
                f.write(r.content)

    def scrapeMarketPrices(self):
        ids = ['7165256','33222657']
        names = ['S&P','c25']

        for i in range(0, len(ids)):
            print(i, "/", len(ids))
            link = "http://euroinvestor.com/stock/historicalquotes.aspx?instrumentId={}&amp;format=CSV".format(ids[i])
            r = requests.get(link)
            with open(r"{0}/{1}.csv".format(self.data_path + '/markets', names[i].replace("/", "")), 'wb') as f:
                f.write(r.content)