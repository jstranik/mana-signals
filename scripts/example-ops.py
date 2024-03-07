import numpy as np

class InputOp:
    """ reads a message from the input """
    def __init__(self):
        self.dtype = dict
        self.value = {}
        self.inputs = []

    def update(self, message: dict):
        self.value = message

class GetOp:
    """ reads a field from the input message """
    def __init__(self, field: str, dtype: np.dtype, inputs: list):
        self.field = field
        self.dtype = dtype
        self.value = dtype()
        self.inputs = inputs

    def update(self, message: dict):
        self.value = self.dtype(message[self.field])

class DiffOp:
    """ computes the difference between the current and last value """
    def __init__(self, dtype: np.dtype, inputs: list):
        self.dtype = dtype
        self.value = dtype()
        self.last = dtype()
        self.inputs = inputs
    
    def update(self, x):
        self.value = x - self.last
        self.last = x

class SignalSetCalculator:
    def __init__(self):
        self.input = InputOp()
        self.lastTradePrice = GetOp("price", np.float64, ["input"])
        self.lastTradeAmount = GetOp("amount", np.float64, ["input"])
        self.dTradePrice = DiffOp(np.float64, ["lastTradePrice"])
        self.dTradeAmount = DiffOp(np.float64, ["lastTradeAmount"])

    def updatesignal(self, signal):
        signal.update(*[getattr(self, x).value for x in signal.inputs])

    def update(self, message: dict):
        self.input.update(message)
        self.updatesignal(self.lastTradePrice)
        self.updatesignal(self.lastTradeAmount)
        self.updatesignal(self.dTradePrice)
        self.updatesignal(self.dTradeAmount)

    def get(self):
        return np.array([
            self.lastTradePrice.value, self.lastTradeAmount.value, self.dTradePrice.value, self.dTradeAmount.value,
            ], dtype=np.float64)


if __name__ == "__main__":
    """ USAGE: `gunzip -c marketdata/20231101.OP.csv.gz | python3 example-ops.py` """
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
        
