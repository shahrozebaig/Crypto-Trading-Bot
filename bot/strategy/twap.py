import time
from ..logger import logger

class TWAPStrategy:
    def __init__(self, orders, symbol, side, qty, parts, interval):
        self.orders = orders
        self.symbol = symbol
        self.side = side
        self.qty = qty
        self.parts = parts
        self.interval = interval

    def execute(self):
        logger.info("TWAP started")
        slice_qty = self.qty / self.parts

        for i in range(self.parts):
            self.orders.place_market_order(self.symbol, self.side, slice_qty)
            logger.info("TWAP slice %s executed", i+1)
            if i < self.parts - 1:
                time.sleep(self.interval)

        logger.info("TWAP complete")
