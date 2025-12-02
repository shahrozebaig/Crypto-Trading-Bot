from .utils import validate_symbol, validate_side, validate_positive_number
from .exceptions import OrderError
from .logger import logger

class OrdersManager:
    def __init__(self, client):
        self.client = client
    def _fix_precision(self, qty):
        return float(f"{float(qty):.3f}")
    def _check_notional(self, qty, price=None):
        if price is None:
            return
        notional = float(qty) * float(price)
        if notional < 100:
            raise OrderError({"msg": f"Order notional ${notional:.2f} < $100 minimum"})

    def place_market_order(self, symbol, side, quantity):
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        qty = self._fix_precision(validate_positive_number(quantity, "quantity"))
        logger.info("Placing MARKET %s %s %s", side, qty, symbol)
        try:
            return self.client.place_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty
            )
        except Exception as e:
            logger.error("Market order failed")
            raise OrderError(e)

    def place_limit_order(self, symbol, side, quantity, price):
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        qty = self._fix_precision(validate_positive_number(quantity, "quantity"))
        price = validate_positive_number(price, "price")
        self._check_notional(qty, price)
        logger.info("Placing LIMIT %s %s @ %s", side, qty, price)
        try:
            return self.client.place_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=qty,
                price=price,
                timeInForce="GTC"
            )
        except Exception as e:
            logger.error("Limit order failed")
            raise OrderError(e)

    def place_stop_limit(self, symbol, side, quantity, stop_price, limit_price):
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        qty = self._fix_precision(validate_positive_number(quantity, "quantity"))
        stop_price = validate_positive_number(stop_price, "stop_price")
        limit_price = validate_positive_number(limit_price, "limit_price")
        self._check_notional(qty, limit_price)
        logger.info(
            "Placing STOP LIMIT %s %s stop=%s limit=%s",
            side, qty, stop_price, limit_price
        )
        try:
            return self.client.place_order(
                symbol=symbol,
                side=side,
                type="STOP",
                quantity=qty,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce="GTC"
            )
        except Exception as e:
            logger.error("Stop-limit order failed")
            raise OrderError(e)
    def place_oco(self, symbol, side, quantity, limit_price, stop_price, stop_limit_price):
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        qty = self._fix_precision(validate_positive_number(quantity, "quantity"))
        limit_price = validate_positive_number(limit_price, "limit_price")
        stop_price = validate_positive_number(stop_price, "stop_price")
        stop_limit_price = validate_positive_number(stop_limit_price, "stop_limit_price")
        self._check_notional(qty, limit_price)
        logger.info("Placing OCO (simulated TP/SL orders)")
        tp_side = "SELL" if side == "BUY" else "BUY"
        try:
            limit_order = self.client.place_order(
                symbol=symbol,
                side=tp_side,
                type="LIMIT",
                quantity=qty,
                price=limit_price,
                timeInForce="GTC"
            )
            stop_order = self.client.place_order(
                symbol=symbol,
                side=tp_side,
                type="STOP",
                quantity=qty,
                stopPrice=stop_price,
                price=stop_limit_price,
                timeInForce="GTC"
            )
            return {
                "limit_order": limit_order,
                "stop_order": stop_order
            }
        except Exception as e:
            logger.error("OCO placement failed")
            raise OrderError(e)
