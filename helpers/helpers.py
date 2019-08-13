import pandas as pd

def get_mail_list():
    return ["jacwar@um.dk", "frewar1905@gmail.com", "skou95@hotmail.com", "amrahbak@gmail.com","chrwar02@gmail.com",
           "Johan.b.33@hotmail.com"]

def get_plots_path():
    return "/Users/frederikwarburg/Desktop/stocks/plots"

def get_stock_data():
    data = pd.read_csv('/Users/frederikwarburg/Desktop/stockIDs.csv')
    ids = data["instrumentid"]
    names = data["instrumentname"]
    return names, ids


# Create crontab command:
# env EDITOR=nano crontab -e
# http://www.techradar.com/how-to/computing/apple/terminal-101-creating-cron-jobs-1305651
