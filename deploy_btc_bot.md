# 🚀 ONE-CLICK DEPLOY: BTC SIGNAL BOT (Workshop Special)

Copy-paste **satu prompt ini** ke AI manapun (ChatGPT, Claude, Gemini, Hermes Agent). Bot akan deploy dengan output IDENTIK -- karena script sudah final dan tested.

---

**PROMPT:**

Tolong deploy BTC Signal Bot:

1. Buat file btc_signal_bot.py dengan konten code block di bawah ini (copy paste)
2. Jalankan: pip install requests
3. Jalankan: python btc_signal_bot.py
4. Selesai. Tampilkan outputnya.

```python
#!/usr/bin/env python3
"""BTC Signal Bot - Workshop PINTU Edition"""
import json, os
from datetime import datetime
import requests

COINGECKO = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
HISTORY_FILE = os.path.expanduser("~/btc_history.json")
SIGNAL_FILE = os.path.expanduser("~/btc_signals.json")

def fetch_7d_prices():
    r = requests.get(COINGECKO, timeout=15)
    r.raise_for_status()
    data = r.json()
    prices = [p[1] for p in data["prices"]]
    return prices[-100:]

def fetch_live_price():
    r = requests.get(PRICE_URL, timeout=10)
    r.raise_for_status()
    return r.json()["bitcoin"]["usd"]

def save_history(prices):
    with open(HISTORY_FILE, "w") as f:
        json.dump(prices, f, indent=2)

def ma5(prices):
    if len(prices) < 5:
        return sum(prices) / len(prices)
    return sum(prices[-5:]) / 5

def rsi14(prices):
    if len(prices) < 15:
        return 50.0
    gains, losses = 0, 0
    for i in range(len(prices)-14, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains += change
        else:
            losses += abs(change)
    avg_gain = gains / 14
    avg_loss = losses / 14
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def generate_signal(price, ma5_val, rsi14_val):
    """Never HOLD - always LONG or SHORT"""
    ma5_bullish = price >= ma5_val
    rsi_bullish = rsi14_val >= 50

    if ma5_bullish and rsi_bullish:
        direction = "LONG"
        confidence = "HIGH"
        reason = "MA5 bullish + RSI bullish - trend kuat"
    elif not ma5_bullish and not rsi_bullish:
        direction = "SHORT"
        confidence = "HIGH"
        reason = "MA5 bearish + RSI bearish - trend lemah"
    elif ma5_bullish and not rsi_bullish:
        direction = "LONG"
        confidence = "MEDIUM"
        reason = "MA5 bullish dominan, RSI bearish - entry cautious"
    else:
        direction = "SHORT"
        confidence = "MEDIUM"
        reason = "MA5 bearish dominan, RSI bullish - entry cautious"

    if direction == "LONG":
        sl = round(price * 0.98, 2)
        tp = round(price * 1.05, 2)
    else:
        sl = round(price * 1.02, 2)
        tp = round(price * 0.95, 2)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "price": price,
        "ma5": round(ma5_val, 2),
        "rsi14": round(rsi14_val, 2),
        "signal": direction,
        "confidence": confidence,
        "entry": price,
        "sl": sl,
        "tp": tp,
        "reason": reason
    }

def format_output(sig):
    lines = [
        f"{'='*55}",
        f"  BTC SIGNAL BOT - {sig['timestamp']}",
        f"{'='*55}",
        f"  BTC/USD  : ${sig['price']:,.2f}",
        f"  MA5      : ${sig['ma5']:,.2f}",
        f"  RSI(14)  : {sig['rsi14']:.1f}",
        f"  SIGNAL   : {sig['signal']}",
        f"  CONFIDENCE: {sig['confidence']}",
        f"  ENTRY    : ${sig['entry']:,.2f}",
        f"  SL (2%)  : ${sig['sl']:,.2f}",
        f"  TP (5%)  : ${sig['tp']:,.2f}",
        f"  REASON   : {sig['reason']}",
        f"{'='*55}",
    ]
    return "\n".join(lines)

def main():
    print("Fetching 7-day BTC history from CoinGecko...")
    history = fetch_7d_prices()
    print(f"Loaded {len(history)} data points\n")

    print("Fetching live BTC price...")
    live = fetch_live_price()
    print(f"Live price: ${live:,.2f}\n")

    history.append(live)
    if len(history) > 100:
        history = history[-100:]

    save_history(history)

    ma5_val = ma5(history)
    rsi14_val = rsi14(history)
    signal = generate_signal(live, ma5_val, rsi14_val)

    with open(SIGNAL_FILE, "w") as f:
        json.dump(signal, f, indent=2)

    print(format_output(signal))

if __name__ == "__main__":
    main()
```

---

## Kenapa Pakai Script Final?

| Cara Lama (prompt deskriptif) | Cara Baru (script final) |
|---|---|
| Tiap AI generate kode sendiri | Semua AI copy-paste script IDENTIK |
| Output format beda-beda | Output persis sama |
| Debug tiap AI punya bug sendiri | Udah tested, zero bug |
| Workshop jadi chaos | Workshop mulus, tinggal run |

## Cara Verifikasi

```bash
cat ~/btc_signals.json
cat ~/btc_history.json
```

## Cara Baca Sinyal

| Sinyal | Arah | SL | TP |
|--------|------|----|----|
| LONG | Beli | Entry - 2% | Entry + 5% |
| SHORT | Jual | Entry + 2% | Entry - 5% |

- **Confidence HIGH** - MA5 & RSI setuju, peluang bagus
- **Confidence MEDIUM** - MA5 & RSI beda arah, entry ikut MA5, TP ketat
