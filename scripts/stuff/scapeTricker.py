import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


data = pd.read_csv('/Users/frederikwarburg/Desktop/stockIDs.csv')
ids = data["instrumentid"]
names = data["instrumentname"]

with open('/Users/frederikwarburg/Desktop/Tickers.csv', 'w') as export:
    export.write('instrumentid,instrumentname, Trickers\n')
    i = 0
    for name in names:
        print(name)
        searchname = name.replace("Ø","o")
        searchname = name.lower()
        searchname = searchname.replace("æ","ae").replace(" b ", " ")\
            .replace(" a ", " ").replace("a.p.","ap").replace("å","aa").replace("a/s b","a/s")\
            .replace("ø","oe").replace("a/s a","a/s").replace(" ","+").replace("ó","o").replace("ö","o")\
            .replace("ü","u").replace("pr&#2","").replace("+og+", "+&+").replace("ser","").replace("brdr","broedr")\
            .replace("sjaelland-fyn+a/s","sjaelland").replace("plc+a","plc").replace("capital+a/s+stam","capital+a/s")\
            .replace("dlh+a/s","dlh").replace("+se", "").replace("+ab+b", "+ab")\
            .replace("+ab+pref", "+ab").replace("+ab+a", " ab").replace("ab+pr", "ab")

        link = "https://markets.ft.com/data/search?assetClass=Equity&query={}".format(searchname)
        html = urllib.request.urlopen(link)
        soup = BeautifulSoup(html, "lxml")
        html.close()
        ticker = soup.find_all('td',{'class': 'mod-ui-table__cell--text'})
        if len(ticker) > 0:
            ticker = ticker[1].text
        else:
            print(name, searchname, ticker)

        export.write('{1},{0},{2}\n'.format(name,ids[i],ticker))
        i = i +1