
class Portefolio:
    def __init__(self):

        self.cash = 100000.0
        self.deposit = {}
        self.trade_cost = 29.0

    def get_value(self, data):

        value = self.cash
        for stock in self.deposit:
            amount, purchase_price = self.deposit[stock]
            current_price = data[stock]['Close Price'][0]
            value += current_price * amount

        return value

    def get_deposit(self):
        return self.deposit

    def get_stock(self, name):

        if name in self.deposit:
            return self.deposit[name]
        else:
            print('not in you deposit')

    def buy(self, name, amount, price):

        if self.cash > amount * price + self.trade_cost:
            if name in self.deposit:
                self.deposit[name] = (self.deposit[name][0] + amount, 1.0 / self.deposit[name][0] + amount * (self.deposit[name][0]*self.deposit[name][1] + amount*price))
            else:
                self.deposit[name] = (amount, price)
            self.cash -= amount*price + self.trade_cost
        else:
            print('Not enough cash')

    def sell(self, name, amount, price):

        if name not in self.deposit: print("You don't own that stock")

        if self.deposit[name][0] == amount:
            del self.deposit[name]
            self.cash += amount * price - self.trade_cost
        elif amount < self.deposit[name][0]:
            self.deposit[name][0] -= amount
            self.cash += amount * price - self.trade_cost
        else:
            print('You do not own that many')




