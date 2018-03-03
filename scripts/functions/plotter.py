import matplotlib.pyplot as plt

def plot_last_x_days(stock, days):
    plt.plot(stock["Date"][len(stock["Date"]) - days:len(stock["Date"])],
             stock["Close Price"][len(stock["Close Price"]) - days:len(stock["Close Price"])])
    plt.title("{0} last {1} days".format(stock, days))
    return plt


def plot_sma(date, price, short_rolling, long_rolling, days_since_gc, date_gc, days_since_dc, date_dc):

    short_window = 50
    long_window = 200

    plt.plot(date.dt.date.values, price, label='Closing price')
    plt.plot(date.dt.date.values[0:(-(short_window - 1))], short_rolling, label='50 days moving average')
    plt.plot(date.dt.date.values[0:(-(long_window - 1))], long_rolling, label='200 days moving average')

    if days_since_gc != -1:
        plt.axvline(date_gc, color = 'green', linestyle='dashed', label='golden cross')
    if days_since_dc != -1:
        plt.axvline(date_dc, color = 'red', linestyle='dashed', label='dead cross')

    plt.legend(loc='upper left')
    plt.ylabel('Price')
    plt.xlabel('Date')

    return plt

def save_plt(plt, path_with_extention):
    plt.savefig(path_with_extention)
    plt.close()
