from bs4 import BeautifulSoup
import urllib.request
import csv


instrumentids = []
instrumentnames = []

indexs = ["http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omx-c25",
         "http://www.euroinvestor.dk/markeder/aktier/europa/danmark/omxc-large-cap",
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
          "http://www.euroinvestor.dk/markeder/aktier/nordamerika/usa/sp-500"]


with open('/Users/frederikwarburg/Desktop/stockIDs.csv', 'w') as export:
    export.write('instrumentid,instrumentname\n')

    for index in indexs:
        html = urllib.request.urlopen(index)
        soup = BeautifulSoup(html, "lxml")
        html.close()

        ids = soup.find_all('img', id="imgContextMenu")
        for id in ids:
            export.write('{1},{0}\n'.format(id['instrumentname'].replace(',',''),id['instrumentid']))