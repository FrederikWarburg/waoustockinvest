import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

data = pd.read_csv('/Users/frederikwarburg/Desktop/Tickers.csv')
print(data)
ids = data["instrumentid"]
names = data["instrumentname"]
tickers = data[" Trickers"]

for ticker in tickers:
    link = "https://markets.ft.com/data/equities/tearsheet/profile?s={}".format(ticker.replace(" ","%20"))
    html = urllib.request.urlopen(link)
    soup = BeautifulSoup(html, "lxml")
    html.close()
    p = soup.find('p',{'class': 'mod-tearsheet-profile-description mod-tearsheet-profile-section'})
    if p!=None:
        with open('/Users/frederikwarburg/Desktop/Stocks/Descriptions/{}.txt'.format(ticker.replace(":","")), 'w') as export:
            export.write(p.text)
    else:
        with open('/Users/frederikwarburg/Desktop/Stocks/Descriptions/{}.txt'.format(ticker.replace(":","")), 'w') as export:
            export.write("Sorry - Missing description")
        export.close()
        print("Missing description on {}".format(ticker))