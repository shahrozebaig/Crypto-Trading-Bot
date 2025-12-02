import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from .logger import logger
from .exceptions import APIError

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, base_url, recv_window=10000):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.recv_window = recv_window
        self.time_offset = self._calculate_time_offset()
        logger.debug("Client initialized (base_url=%s)", self.base_url)

    def _calculate_time_offset(self):
        """Fetch server time and compare with local time."""
        try:
            resp = requests.get(self.base_url + "/fapi/v1/time", timeout=5)
            server_time = resp.json().get("serverTime")
            local_time = int(time.time() * 1000)
            return server_time - local_time
        except Exception as e:
            logger.warning("Time offset fetch failed: %s", e)
            return 0

    def _timestamp(self):
        """Return local time corrected by server offset."""
        return int(time.time() * 1000) + self.time_offset

    def _sign(self, params):
        params["timestamp"] = self._timestamp()
        params["recvWindow"] = self.recv_window

        query = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()

        params["signature"] = signature
        return params

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def _request(self, method, path, signed=False, params=None):
        """Safely perform a Binance API request."""
        if params is None:
            params = {}

        url = self.base_url + path

        if signed:
            params = self._sign(params)

        try:
            logger.debug("REQ -> %s %s %s", method, url, params)
            response = requests.request(method, url, params=params, headers=self._headers())
            logger.debug("RESP <- %s %s", response.status_code, response.text)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            try:
                err = response.json()
            except:
                err = {"msg": "Unknown Binance error"}
            logger.error("HTTP ERROR: %s", err)
            raise APIError(err)
        except Exception as e:
            logger.error("Request failed: %s", str(e))
            raise APIError({"msg": str(e)})

    def place_order(self, **params):
        return self._request("POST", "/fapi/v1/order", signed=True, params=params)

    def get_order(self, **params):
        return self._request("GET", "/fapi/v1/order", signed=True, params=params)

    def cancel_order(self, **params):
        return self._request("DELETE", "/fapi/v1/order", signed=True, params=params)

    def get_positions(self):
        return self._request("GET", "/fapi/v2/positionRisk", signed=True)

    def get_price(self, symbol):
        return self._request("GET", "/fapi/v1/ticker/price", signed=False, params={"symbol": symbol})
