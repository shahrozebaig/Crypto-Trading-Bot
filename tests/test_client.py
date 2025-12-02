from bot.client import BinanceFuturesClient

def test_client_timestamp_offset():
    c = BinanceFuturesClient("key", "secret", "https://testnet.binancefuture.com")
    assert isinstance(c.time_offset, int)
