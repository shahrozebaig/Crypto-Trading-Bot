from bot.strategy.twap import TWAPStrategy
from bot.strategy.grid import GridStrategy

class DummyOrders:
    def place_market_order(self, symbol, side, qty):
        return {"symbol": symbol, "side": side, "qty": qty}

    def place_limit_order(self, symbol, side, qty, price):
        return {"symbol": symbol, "side": side, "qty": qty, "price": price}

def test_twap():
    strat = TWAPStrategy(DummyOrders(), "BTCUSDT", "BUY", 1, 2, 1)
    assert True

def test_grid():
    strat = GridStrategy(DummyOrders(), "BTCUSDT", "BUY", 10, 20, 3, 0.1)
    result = strat.execute()
    assert len(result) == 3
