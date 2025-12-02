import numpy as np
from ..logger import logger

class GridStrategy:
    def __init__(self, orders, symbol, side, lower, upper, steps, qty):
        self.orders = orders
        self.symbol = symbol
        self.side = side
        self.lower = lower
        self.upper = upper
        self.steps = steps
        self.qty = qty

    def execute(self):
        prices = np.linspace(self.lower, self.upper, self.steps)
        logger.info("Grid strategy running")

        results = []
        for p in prices:
            res = self.orders.place_limit_order(self.symbol, self.side, self.qty, p)
            results.append(res)

        return results
