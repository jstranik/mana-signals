import numpy as np

class SignalSetCalculator:
    def __init__(self):
        self.lastTradePrice: float = np.nan
        self.lastTradeAmount: float = np.nan
        self.dTradePrice: float = 0.
        self.dTradeAmount: float = 0.

    def update(self, message: dict):
        px = message['price']
        amt = message['amount']

        self.dTradePrice = px - self.lastTradePrice
        self.dTradeAmount = amt - self.lastTradeAmount
        self.lastTradePrice = px
        self.lastTradeAmount = amt
    
    def get(self):
        return np.array([
            self.lastTradePrice, self.lastTradeAmount, self.dTradePrice, self.dTradeAmount,
            ], dtype = np.float64)


if __name__ == "__main__":
    """ USAGE: `gunzip -c marketdata/20231101.OP.csv.gz | python3 example-inline.py` """
    fc = SignalSetCalculator()
    input()
    i = 0
    while True:
        i += 1
        ls = input().strip().split(",")
        message = {
            "exchange": ls[0],
            "symbol": ls[1],
            "local_timestamp": np.datetime64(ls[3], "ns"),
            "side": ls[5],
            "price": float(ls[6]),
            "amount": float(ls[7])
        }
        fc.update(message)
        if i % 1000 == 0:
            print(fc.get())
        
