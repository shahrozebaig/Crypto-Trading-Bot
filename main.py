import argparse
import os
from dotenv import load_dotenv
from rich import print
from bot.logger import setup_logger, logger
from bot.client import BinanceFuturesClient
from bot.orders import OrdersManager
from bot.strategy.twap import TWAPStrategy
from bot.strategy.grid import GridStrategy
load_dotenv()
def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--api_key", default=os.getenv("BINANCE_API_KEY"))
    p.add_argument("--api_secret", default=os.getenv("BINANCE_API_SECRET"))
    p.add_argument("--base_url", default=os.getenv("BASE_URL"))
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("market")
    m.add_argument("--symbol", required=True)
    m.add_argument("--side", required=True)
    m.add_argument("--quantity", required=True)

    l = sub.add_parser("limit")
    l.add_argument("--symbol", required=True)
    l.add_argument("--side", required=True)
    l.add_argument("--quantity", required=True)
    l.add_argument("--price", required=True)

    s = sub.add_parser("stop")
    s.add_argument("--symbol", required=True)
    s.add_argument("--side", required=True)
    s.add_argument("--quantity", required=True)
    s.add_argument("--price", required=True)
    s.add_argument("--stop_price", required=True)

    o = sub.add_parser("oco")
    o.add_argument("--symbol", required=True)
    o.add_argument("--side", required=True)
    o.add_argument("--quantity", required=True)
    o.add_argument("--limit_price", required=True)
    o.add_argument("--stop_price", required=True)
    o.add_argument("--stop_limit_price", required=True)

    t = sub.add_parser("twap")
    t.add_argument("--symbol", required=True)
    t.add_argument("--side", required=True)
    t.add_argument("--quantity", required=True, type=float)
    t.add_argument("--parts", type=int, default=5)
    t.add_argument("--interval", type=int, default=10)

    g = sub.add_parser("grid")
    g.add_argument("--symbol", required=True)
    g.add_argument("--side", required=True)
    g.add_argument("--lower", required=True, type=float)
    g.add_argument("--upper", required=True, type=float)
    g.add_argument("--steps", required=True, type=int)
    g.add_argument("--quantity", required=True, type=float)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    setup_logger()
    client = BinanceFuturesClient(args.api_key, args.api_secret, args.base_url)
    orders = OrdersManager(client)
    if args.cmd == "market":
        print(orders.place_market_order(args.symbol, args.side, args.quantity))
    elif args.cmd == "limit":
        print(orders.place_limit_order(args.symbol, args.side, args.quantity, args.price))
    elif args.cmd == "stop":
        print(orders.place_stop_limit(args.symbol, args.side, args.quantity, args.stop_price, args.price))
    elif args.cmd == "oco":
        print(orders.place_oco(args.symbol, args.side, args.quantity, args.limit_price, args.stop_price, args.stop_limit_price))
    elif args.cmd == "twap":
        TWAPStrategy(orders, args.symbol, args.side, args.quantity, args.parts, args.interval).execute()
    elif args.cmd == "grid":
        GridStrategy(orders, args.symbol, args.side, args.lower, args.upper, args.steps, args.quantity).execute()
if __name__ == "__main__":
    main()