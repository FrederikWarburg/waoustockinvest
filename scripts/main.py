
from functions.loadAllStocks import *
from functions.SMA import *


#downloadStocks()
data = loadStocks()
check_crossovers_c25(data)

#names, ids = get_stock_data()

