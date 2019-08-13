from Helper import *
import pandas as pd
import requests


class c25:
    def __init__(self):

        self.data_path = "/Users/frederikwarburg/Desktop/stocks/data"
        self.c25 = ["APMA", "APMB", "BA", "CA", "CRH", "COL", "DB", "DSV", "FLS", "GM", "GNS", "ISS", "JB",
                    "LUN", "NETS", "NKT", "NB", "NN", "NO", "PAN", "TDC", "TRY", "VES", "WI", "OE"]

    def downloadc25(self):
        APMA = "/stock/historicalquotes.aspx?instrumentId=395357&amp;format=CSV"
        APMB = "/stock/historicalquotes.aspx?instrumentId=395356&amp;format=CSV"
        BA = "/stock/historicalquotes.aspx?instrumentId=205512&amp;format=CSV"
        CA = "/stock/historicalquotes.aspx?instrumentId=205057&amp;format=CSV"
        CRH = "/stock/historicalquotes.aspx?instrumentId=2337926&amp;format=CSV"
        COL = "/stock/historicalquotes.aspx?instrumentId=206388&amp;format=CSV"
        DB = "/stock/historicalquotes.aspx?instrumentId=235240&amp;format=CSV"
        DSV = "/stock/historicalquotes.aspx?instrumentId=335810&amp;format=CSV"
        FLS = "/stock/historicalquotes.aspx?instrumentId=205618&amp;format=CSV"
        GM = "/stock/historicalquotes.aspx?instrumentId=235621&amp;format=CSV"
        GNS = "/stock/historicalquotes.aspx?instrumentId=203359&amp;format=CSV"
        ISS = "/stock/historicalquotes.aspx?instrumentId=205491&amp;format=CSV"
        JB = "/stock/historicalquotes.aspx?instrumentId=206220&amp;format=CSV"
        LUN = "/stock/historicalquotes.aspx?instrumentId=204900&amp;format=CSV"
        NETS = "/stock/historicalquotes.aspx?instrumentId=32651003&amp;format=CSV"
        NKT = "/stock/historicalquotes.aspx?instrumentId=205239&amp;format=CSV"
        NB = "/stock/historicalquotes.aspx?instrumentId=242556&amp;format=CSV"
        NN = "/stock/historicalquotes.aspx?instrumentId=205365&amp;format=CSV"
        NO = "/stock/historicalquotes.aspx?instrumentId=239698&amp;format=CSV"
        PAN = "/stock/historicalquotes.aspx?instrumentId=2632080&amp;format=CSV"
        TDC = "/stock/historicalquotes.aspx?instrumentId=275952&amp;format=CSV"
        TRY = "/stock/historicalquotes.aspx?instrumentId=511785&amp;format=CSV"
        VES = "/stock/historicalquotes.aspx?instrumentId=206326&amp;format=CSV"
        WI = "/stock/historicalquotes.aspx?instrumentId=205058&amp;format=CSV"
        OE = "/stock/historicalquotes.aspx?instrumentId=34573954&amp;format=CSV"

        c20 = "/stock/historicalquotes.aspx?instrumentId=6313776&amp;format=CSV"

        C25 = [APMA, APMB, BA, CA, CRH, COL, DB, DSV, FLS, GM, GNS, ISS, JB, LUN, NETS, NKT, NB, NN, NO, PAN, TDC, TRY,
               VES, WI, OE]

        C25s = self.get_c25()

        for i in range(len(C25)):
            r = requests.get("http://euroinvestor.com{}".format(C25[i]))

            with open("{0}/stock{1}.csv".format(self.get_data_path(), C25s[i]), 'wb') as f:
                f.write(r.content)

        r = requests.get("http://euroinvestor.com{}".format(c20))
        with open("{0}/stock{1}.csv".format(self.get_data_path(), "c20"), 'wb') as f:
            f.write(r.content)

    def loadc25(self):
        C25s = self.get_c25()

        data = {}

        for company in C25s:
            tmp = pd.read_csv('{0}/stock{1}.csv'.format(self.get_data_path(), company))
            date = tmp["Date"]
            date_f = []
            for i in range(len(date)):
                date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
            tmp["Date"] = date_f
            tmp = tmp.drop('Unnamed: 6', 1)
            data.update({company: tmp})

        return data

    def loadc20(self):
        data = pd.read_csv('{0}/stock{1}.csv'.format(self.get_data_path(), "c20"))
        date = data["Date"]
        date_f = []
        for i in range(len(date)):
            date_f.append(pd.to_datetime(date[i][:10], format="%d/%m/%Y"))
        data["Date"] = date_f
        data = data.drop('Unnamed: 6', 1)

        return data

