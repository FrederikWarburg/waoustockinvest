import pandas as pd

data = pd.read_csv('/Users/frederikwarburg/Desktop/stockIDs.csv')

print(len(data["instrumentid"]))
