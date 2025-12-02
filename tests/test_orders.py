from bot.orders import OrdersManager
from bot.client import BinanceFuturesClient

class DummyClient:
    def place_order(self, **params):
        return params

def test_market_order():
    o = OrdersManager(DummyClient())
    res = o.place_market_order("BTCUSDT", "BUY", 1)
    assert res["type"] == "MARKET"
