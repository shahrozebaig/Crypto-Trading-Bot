import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
load_dotenv()
from bot.client import BinanceFuturesClient
from bot.orders import OrdersManager
app = Flask(__name__, static_folder="web", template_folder="web")
client = BinanceFuturesClient(
    os.getenv("BINANCE_API_KEY"),
    os.getenv("BINANCE_API_SECRET"),
    os.getenv("BASE_URL")
)
orders = OrdersManager(client)
@app.route("/")
def index():
    return send_from_directory("web", "index.html")
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("web", path)
@app.route("/api/price", methods=["GET"])
def api_price():
    try:
        symbol = request.args.get("symbol", "BTCUSDT")
        data = client.get_price(symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify({"price": None, "error": str(e)})
@app.route("/api/positions", methods=["GET"])
def api_positions():
    try:
        positions = client.get_positions()
        return jsonify(positions)
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/api/order", methods=["POST"])
def api_order():
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        side = data.get("side")
        order_type = data.get("orderType")
        qty = float(data.get("qty"))
        price = data.get("price")
        stop_price = data.get("stop_price")
        if order_type == "MARKET":
            resp = orders.place_market_order(symbol, side, qty)
        elif order_type == "LIMIT":
            resp = orders.place_limit_order(symbol, side, qty, price)
        elif order_type == "STOP":
            resp = orders.place_stop_limit(symbol, side, qty, stop_price, price)
        else:
            return jsonify({"error": "Invalid order type"}), 400
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == "__main__":
    print("🚀 UI Server running at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
