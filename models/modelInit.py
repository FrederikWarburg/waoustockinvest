from models.CAPM import CAPM
from models.market import Market
from models.model import Model
from models.SMA import SMA
from models.prophet import PROPHET

def modelInitializer(name, portefolio):

    if name == 'MARKET':
        return Market(portefolio)
    elif name == 'SMA':
        return SMA(portefolio)
    elif name == 'CAPM':
        return CAPM(portefolio)
    elif name == 'PROPHET':
        return PROPHET(portefolio)
    elif name == 'XGBOOST':
        pass
    elif name == 'Linear':
        pass
    elif name == 'MA':
        pass
    elif name == 'LSTM':
        pass
    elif name == 'KNN':
        pass
    elif name == 'ARIMA':
        pass
    elif name == 'NN':
        pass
    elif name == 'momentum':
        pass

    #https://github.com/borisbanushev/stockpredictionai