#!/usr/bin/env python3
"""
FROM ZERO TO TRADING BOTS — Workshop PINTU × Web3 Dev Bandung
============================================================
Bot sederhana: ambil harga → hitung indikator → generate sinyal.
Ganti `fetch_price()` dengan API real nanti.
"""

import json, math, urllib.request
from datetime import datetime, timezone, timedelta

# ─── Config ───
COOLDOWN_HRS = 4
MAX_HIST = 100

INDICATORS = {
    "RSI": "Relative Strength Index — ukur kecepatan perubahan harga",
    "EMA": "Exponential Moving Average — rata-rata harga terbobot",
    "MACD": "Moving Average Convergence Divergence — momentum",
    "BB": "Bollinger Bands — volatility envelope",
    "ATR": "Average True Range — volatilitas untuk SL/TP",
}

# ─── Price Fetch ───
def fetch_price():
    """
    TODO: Ganti dengan API real:
    - Kitco: https://www.kitco.com/charts/gold
    - Binance: https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT
    - CCXT: library Python untuk 100+ exchange

    Return: dict {bid: float, ask: float, change_pct: float}
    """
    # Demo data — diganti peserta nanti
    return {"bid": 4075.70, "ask": 4076.10, "change_pct": 1.71, "timestamp": datetime.now().isoformat()}


# ─── Helper ───
def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ─── Indicator 1: RSI ───
def calc_rsi(prices, period=14):
    """RSI > 70 = overbought (sinyal SHORT). RSI < 30 = oversold (sinyal LONG)."""
    if len(prices) < period + 1:
        return 50.0
    gains = losses = 0.0
    for i in range(-period, 0):
        d = prices[i] - prices[i - 1]
        if d >= 0:
            gains += d
        else:
            losses -= d
    ag = gains / period
    al = losses / period
    if al == 0:
        return 100.0
    rs = ag / al
    return 100.0 - (100.0 / (1.0 + rs))


# ─── Indicator 2: EMA ───
def calc_ema(prices, period):
    """EMA9 > EMA21 = bullish (uptrend). EMA9 < EMA21 = bearish (downtrend)."""
    if len(prices) < period:
        return prices[-1] if prices else 0
    k = 2.0 / (period + 1.0)
    ema = sum(prices[-period:]) / period  # seed pakai SMA
    for p in prices[-period:]:
        ema = p * k + ema * (1.0 - k)
    return ema


# ─── Indicator 3: MACD ───
def calc_macd(prices, fast=12, slow=26, signal=9):
    """MACD > 0 = bullish momentum. MACD < 0 = bearish."""
    if len(prices) < slow + signal:
        return 0.0
    ema_f = calc_ema(prices, fast)
    ema_s = calc_ema(prices, slow)
    return ema_f - ema_s


# ─── Indicator 4: Bollinger Bands ───
def calc_bollinger(prices, period=20, std_dev=2.0):
    """Upper band = overbought. Lower band = oversold. Mid = rata-rata."""
    recent = prices[-period:]
    sma = sum(recent) / period
    var = sum((p - sma) ** 2 for p in recent) / period
    std = math.sqrt(var)
    return sma, sma + std_dev * std, sma - std_dev * std


# ─── Indicator 5: ATR ───
def calc_atr(history, period=14):
    """ATR besar = market volatil. ATR kecil = market tenang."""
    if len(history) < period:
        return 10.0
    ranges = []
    for i in range(-period, 0):
        h = history[i].get("high", history[i]["bid"])
        l = history[i].get("low", history[i]["bid"])
        ranges.append(h - l)
    return sum(ranges) / period if ranges else 10.0


# ─── Generate Signal ───
def generate_signal(prices, history, last_signal):
    """
    Combine semua indikator → confidence score 0-100%.
    >=60% → signal LONG/SHORT.
    <60% → skip.
    """

    # Cek cooldown — jangan spam sinyal
    if last_signal and last_signal.get("status") == "active":
        return None  # masih ada posisi aktif

    if last_signal:
        last_time = datetime.fromisoformat(last_signal["timestamp"])
        elapsed = (datetime.now(timezone.utc) - last_time).total_seconds() / 3600
        if elapsed < COOLDOWN_HRS:
            return None  # masih dalam masa cooldown

    price = prices[-1] if isinstance(prices[-1], (int, float)) else prices[-1].get("bid", prices[-1])
    rsi = calc_rsi(prices)
    ema9 = calc_ema(prices, 9)
    ema21 = calc_ema(prices, 21)
    macd = calc_macd(prices)
    bb_mid, bb_up, bb_lo = calc_bollinger(prices)
    atr = calc_atr(history)

    reasons = []
    conf = 50  # base confidence

    # RSI
    if rsi >= 70:
        reasons.append(f"RSI {rsi:.0f}>=70 overbought")
        conf -= 20
    elif rsi <= 30:
        reasons.append(f"RSI {rsi:.0f}<=30 oversold")
        conf += 20
    elif rsi > 50:
        reasons.append(f"RSI {rsi:.0f}>50 bullish bias")
        conf += 5
    else:
        reasons.append(f"RSI {rsi:.0f}<50 bearish bias")
        conf -= 2

    # EMA crossover
    if ema9 > ema21:
        reasons.append("EMA9>21 bullish")
        conf += 12
    else:
        reasons.append("EMA9<21 bearish")
        conf -= 12

    # MACD
    if macd > 0:
        reasons.append("MACD+ bullish momentum")
        conf += 8
    else:
        reasons.append("MACD- bearish momentum")
        conf -= 8

    # Bollinger
    if price <= bb_lo:
        reasons.append(f"BB lower ${bb_lo:.0f} bounce potensial")
        conf += 18
    elif price >= bb_up:
        reasons.append(f"BB upper ${bb_up:.0f} rejection potensial")
        conf -= 18
    elif price > bb_mid:
        reasons.append(f"Price > BB mid ${bb_mid:.0f}")
        conf += 5
    else:
        reasons.append(f"Price < BB mid ${bb_mid:.0f}")
        conf -= 2

    conf = max(0, min(100, conf))

    if conf < 60:
        return None  # confidence terlalu rendah

    direction = "LONG" if conf > 50 else "SHORT"
    sl_dist = atr * 1.5
    tp_dist = atr * 2.5

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "direction": direction,
        "entry": round(price, 2),
        "sl": round(price - sl_dist if direction == "LONG" else price + sl_dist, 2),
        "tp": round(price + tp_dist if direction == "LONG" else price - tp_dist, 2),
        "rr": round(tp_dist / sl_dist, 2),
        "confidence": round(conf),
        "rsi": round(rsi, 1),
        "atr": round(atr, 1),
        "macd": round(macd, 2),
        "bb_mid": round(bb_mid, 2),
        "bb_up": round(bb_up, 2),
        "bb_lo": round(bb_lo, 2),
        "reasons": reasons[:6],
        "status": "active",
        "closed_at": None,
        "exit_price": None,
        "pnl_pct": None,
    }


# ─── Format Output ───
def format_signal(sig, price):
    now = datetime.now(timezone(timedelta(hours=7))).strftime("%d %b %H:%M WIB")
    emoji = "🟢" if sig["direction"] == "LONG" else "🔴"
    lines = [
        f"TRADING SIGNAL — {now}",
        "=" * 40,
        f"Price: ${price['bid']:.2f} ({price['change_pct']:+.2f}%)",
        f"Direction: {emoji} {sig['direction']} | Confidence: {sig['confidence']}%",
        "",
        f"Entry: ${sig['entry']:.2f}",
        f"SL: ${sig['sl']:.2f} | TP: ${sig['tp']:.2f}",
        f"R:R 1:{sig['rr']}",
        "",
        "Indicators:",
        f"  RSI: {sig['rsi']} | ATR: ${sig['atr']:.1f}",
        f"  BB Mid: ${sig['bb_mid']:.1f} | Upper: ${sig['bb_up']:.1f} | Lower: ${sig['bb_lo']:.1f}",
        f"  MACD: {sig['macd']:+.2f}",
        "",
        "Reasons:",
    ]
    for r in sig["reasons"]:
        lines.append(f"  • {r}")
    lines.append("")
    lines.append("⚠️ AI-generated signal. Not financial advice. DYOR.")
    return "\n".join(lines)


# ─── Main ───
def main():
    # 1. Ambil harga
    price = fetch_price()
    if not price:
        print("❌ Gagal ambil harga. Cek koneksi / API.")
        return

    bid = price["bid"]

    # 2. Load history + update
    history = load_json("history.json", [])
    candle = {
        "bid": price["bid"],
        "ask": price["ask"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    history.append(candle)
    if len(history) > MAX_HIST:
        history = history[-MAX_HIST:]
    save_json("history.json", history)

    prices = [h["bid"] for h in history]

    # 3. Load signals
    signals = load_json("signals.json", [])

    # 4. Cek posisi aktif — ada yang kena TP/SL?
    active = [s for s in signals if s.get("status") == "active"]
    for a in active:
        if a["direction"] == "LONG":
            if bid <= a["sl"]:
                a["status"] = "loss"
                a["closed_at"] = datetime.now(timezone.utc).isoformat()
                a["exit_price"] = bid
                a["pnl_pct"] = round((bid - a["entry"]) / a["entry"] * 100, 2)
                print(f"❌ SL HIT — Loss ${bid:.2f}")
            elif bid >= a["tp"]:
                a["status"] = "win"
                a["closed_at"] = datetime.now(timezone.utc).isoformat()
                a["exit_price"] = bid
                a["pnl_pct"] = round((bid - a["entry"]) / a["entry"] * 100, 2)
                print(f"✅ TP HIT — Win ${bid:.2f}")
        else:  # SHORT
            if bid >= a["sl"]:
                a["status"] = "loss"
                a["closed_at"] = datetime.now(timezone.utc).isoformat()
                a["exit_price"] = bid
                a["pnl_pct"] = round((a["entry"] - bid) / a["entry"] * 100, 2)
                print(f"❌ SL HIT — Loss ${bid:.2f}")
            elif bid <= a["tp"]:
                a["status"] = "win"
                a["closed_at"] = datetime.now(timezone.utc).isoformat()
                a["exit_price"] = bid
                a["pnl_pct"] = round((a["entry"] - bid) / a["entry"] * 100, 2)
                print(f"✅ TP HIT — Win ${bid:.2f}")

    save_json("signals.json", signals)

    # 5. Generate sinyal baru
    last_sig = signals[-1] if signals else None
    sig = generate_signal(prices, history, last_sig)

    if sig:
        signals.append(sig)
        save_json("signals.json", signals)
        print(format_signal(sig, price))
    else:
        # Bot silent — itu normal (cooldown / posisi aktif / conf rendah)
        pass


if __name__ == "__main__":
    main()
