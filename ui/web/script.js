document.addEventListener("DOMContentLoaded", () => {
    const orderType = document.getElementById("orderType");
    const priceRow = document.getElementById("priceRow");
    const stopRow = document.getElementById("stopRow");
    const qtyInput = document.getElementById("qty");
    const symbolInput = document.getElementById("symbol");
    const minQtyLabel = document.getElementById("minQtyLabel");
    const qtyWarning = document.getElementById("qtyWarning");
    const livePriceEl = document.getElementById("livePrice");
    const submitBtn = document.getElementById("submitBtn");
    const resultBox = document.getElementById("resultBox");
    const themeToggle = document.getElementById("themeToggle");
    const orderSound = document.getElementById("orderSound");
    const historyTable = document.querySelector("#orderHistory tbody");
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("light");
        themeToggle.textContent =
            document.body.classList.contains("light") ? "☀️" : "🌙";
    });
    function checkQtyWarning() {
        const val = qtyInput.value.trim();
        if (!val) return (qtyWarning.textContent = "");
        const decimals = val.includes(".") ? val.split(".")[1].length : 0;
        qtyWarning.textContent =
            decimals > 3 ? "⚠ Binance max precision is 3 decimals for BTCUSDT" : "";
    }
    qtyInput.addEventListener("input", checkQtyWarning);
    async function updateMinQty() {
        let symbol = symbolInput.value.trim().toUpperCase();
        if (!symbol) return;
        let r = await fetch(`/api/price?symbol=${symbol}`);
        let data = await r.json();
        if (!data.price) return (minQtyLabel.textContent = "Min Qty: --");
        let minQty = (100 / parseFloat(data.price)).toFixed(6);
        minQtyLabel.textContent = `Min Qty: ${minQty}`;
        checkQtyWarning();
    }
    symbolInput.addEventListener("input", updateMinQty);
    qtyInput.addEventListener("input", updateMinQty);
    updateMinQty();
    orderType.addEventListener("change", () => {
        const t = orderType.value;
        priceRow.classList.toggle("hidden", t === "MARKET");
        stopRow.classList.toggle("hidden", t !== "STOP");
    });
    function showToast(message, type = "info") {
        const container = document.getElementById("toastContainer");
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => {
            toast.classList.add("hide");
            setTimeout(() => toast.remove(), 400);
        }, 2500);
    }
    function addOrderHistory(payload) {
        let row = `
            <tr>
                <td>${new Date().toLocaleTimeString()}</td>
                <td>${payload.side}</td>
                <td>${payload.symbol}</td>
                <td>${payload.qty}</td>
                <td>${payload.orderType}</td>
            </tr>
        `;
        historyTable.innerHTML = row + historyTable.innerHTML;
    }
    submitBtn.addEventListener("click", async () => {
        const payload = {
            symbol: symbolInput.value,
            side: document.getElementById("side").value,
            orderType: orderType.value,
            qty: qtyInput.value,
            price: document.getElementById("price").value,
            stop_price: document.getElementById("stop_price").value
        };
        resultBox.textContent = "Placing order...";
        let r = await fetch("/api/order", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        let json = await r.json();
        if (json.error || json.msg || json.code) {
            showToast("❌ " + (json.msg || json.error || "Order Failed"), "error");
        } else {
            showToast(`✅ ORDER: ${payload.side} ${payload.qty} ${payload.symbol}`, "success");
            orderSound.play();          
            addOrderHistory(payload);   
        }
        resultBox.textContent = JSON.stringify(json, null, 2);
        resultBox.scrollTop = 0; 
    });
    async function loadLivePrice() {
        let r = await fetch(`/api/price?symbol=${symbolInput.value}`);
        let data = await r.json();
        livePriceEl.textContent =
            data.price ? "$" + Number(data.price).toFixed(2) : "--";
    }
    setInterval(loadLivePrice, 1000);
    loadLivePrice();
    function loadChart() {
        const container = document.getElementById("tv_chart_container");
        if (!container) return;
        container.innerHTML = "";
        new TradingView.widget({
            autosize: true,
            symbol: "BINANCE:BTCUSDT",
            interval: "1",
            theme: document.body.classList.contains("light") ? "light" : "dark",
            style: "1",
            locale: "en",
            timezone: "Etc/UTC",
            enable_publishing: false,
            allow_symbol_change: true,
            container_id: "tv_chart_container"
        });
    }
    setTimeout(loadChart, 500);
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(x => x.classList.remove("active"));
            btn.classList.add("active");
            const target = btn.dataset.tab;
            document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
            document.getElementById(target).classList.add("active");
        });
    });

});
let depthSocket = null;
let tradesSocket = null;
function startWebSockets() {
    const symbol = document.getElementById("symbol").value.trim().toLowerCase();
    if (depthSocket) depthSocket.close();
    if (tradesSocket) tradesSocket.close();
    depthSocket = new WebSocket(
        `wss://stream.binance.com:9443/ws/${symbol}@depth5@100ms`
    );
    depthSocket.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
        const box = document.getElementById("orderBookBox");
        let bidsHTML = data.bids
            .map(b => `<div class="bid">Bid: ${b[0]} | Qty: ${b[1]}</div>`)
            .join("");
        let asksHTML = data.asks
            .map(a => `<div class="ask">Ask: ${a[0]} | Qty: ${a[1]}</div>`)
            .join("");
        box.innerHTML = `
            <h3>Bids</h3>
            ${bidsHTML}
            <h3 style="margin-top:10px;">Asks</h3>
            ${asksHTML}
        `;
    };
    tradesSocket = new WebSocket(
        `wss://stream.binance.com:9443/ws/${symbol}@trade`
    );
    tradesSocket.onmessage = (msg) => {
        const t = JSON.parse(msg.data);
        const box = document.getElementById("tradesBox");
        const entry = `
            <div class="trade-row ${t.m ? "sell" : "buy"}">
                Price: ${t.p} | Qty: ${t.q}
            </div>
        `;
        box.innerHTML = entry + box.innerHTML;
        if (box.querySelectorAll(".trade-row").length > 50) {
            box.lastElementChild.remove();
        }
    };
}
setTimeout(startWebSockets, 1000);
document.getElementById("symbol").addEventListener("input", () => {
    setTimeout(startWebSockets, 500);
});
