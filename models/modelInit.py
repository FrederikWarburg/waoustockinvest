from models.CAPM import CAPM
from models.market import Market
from models.model import Model
from models.SMA import SMA

def modelInitializer(name, portefolio):

    if name == 'MARKET':
        return Market(portefolio)
    elif name == 'SMA':
        return SMA(portefolio)
    elif name == 'CAPM':
        return CAPM(portefolio)