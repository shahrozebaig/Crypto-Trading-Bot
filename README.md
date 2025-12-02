# 🚀 Crypto Futures Trading Bot (Binance Testnet)

This project is a simple and complete crypto futures trading bot built for the Binance USDT-M Futures Testnet. It allows users to place futures trades, monitor live market data, and manage positions through a clean Python backend and a real-time web dashboard. The system supports market, limit, and stop-limit orders, automatically checks all inputs, and follows Binance’s trading rules to prevent errors. The dashboard streams live prices, order book data, and recent trades, and includes an integrated TradingView chart for quick market analysis. 

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| 🔌 Backend | Python, Flask |
| 📡 API | Binance REST + WebSocket |
| 📊 Charts | TradingView Library |
| 🎨 Frontend | HTML, CSS, JavaScript |
| 🔄 Real-time | WebSocket Streaming |

---

<img width="989" height="989" alt="Screenshot 2025-12-03 003056" src="https://github.com/user-attachments/assets/02daa8a5-3439-4f4e-b80e-1edd838b29f4" />

### Start the Dashboard

```bash
python -m ui.server
```

Dashboard will be available at:

```
http://127.0.0.1:5000
```

Open your browser and start trading! 🎉

---

### 📊 Market Data

- **Order Book** - Live depth5 WebSocket updates
- **Recent Trades** - Real-time trade feed
- **Price Chart** - TradingView integrated chart with full analysis tools


### 🔔 Notifications

- ✅ **Success** - Green toast + sound alert
- ❌ **Error** - Red toast with Binance error message
- ⏳ **Pending** - Order status updates

---
