# FROM ZERO TO TRADING BOTS — GuideBook

**Workshop PINTU × Web3 Dev Bandung**
Sabtu, 25 Juli 2026 | 13:00 WIB | Parla Cafe, Bandung

---

## Daftar Isi

1. [Persiapan — Install Dari Rumah](#1-persiapan-install-dari-rumah)
2. [Panduan Workshop Lengkap](#2-panduan-workshop-lengkap)
3. [Trading Bot Template (Full Code)](#3-trading-bot-template-full-code)
4. [Cheatsheet Prompt — Modifikasi Bot](#4-cheatsheet-prompt-modifikasi-bot)
5. [Cron & Telegram](#5-cron--telegram)
6. [Troubleshooting](#6-troubleshooting)
7. [Bonus: Belajar Mandiri](#7-bonus-belajar-mandiri)

---

# 1. Persiapan — Install Dari Rumah

WiFi venue mungkin lambat. Install ini dari rumah biar ga buang waktu.

## 1.1 Python 3.10+

**Download:** https://www.python.org/downloads/

Cek setelah install:
```bash
python --version
# Harus: Python 3.10.x atau lebih baru
```

**PENTING:** Centang **"Add Python to PATH"** pas install!

## 1.2 curl

**Windows 10/11:** Sudah include.
Cek:
```bash
curl --version
```

**Mac:** Sudah pre-install.

**Linux:** `sudo apt install curl`

## 1.3 Code Editor

Pilih salah satu:
- **VS Code** — https://code.visualstudio.com/
- **Cursor** — https://cursor.sh/
- **Notepad++** — kalau ringan aja

## 1.4 Daftar OpenRouter (GRATIS)

**Step-by-step:**

1. Buka https://openrouter.ai/keys
2. Klik "Sign Up" — login pake Google / GitHub / email
3. Setelah login, klik **"Create Key"**
4. Nama: `Workshop PINTU` (bebas)
5. Centang semua permission
6. Klik "Create" → **Copy API key** yang muncul
7. Simpan di Notepad — bakal dipake pas workshop

**Kenapa OpenRouter?**
- Gratis — model gratis cukup untuk workshop
- Ga perlu isi saldo/pulsa
- Bisa pake banyak model: DeepSeek, Qwen, Gemini, Llama

**Alternatif (kalau gagal daftar OpenRouter):**
- Gemini API: https://aistudio.google.com/apikey — gratis 60 request/menit
- Ollama (local): install + download model gratis, butuh RAM 8GB+

## 1.5 Install Hermes Agent

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Cek:
```bash
hermes doctor
```

> **Catatan Windows:** Butuh PowerShell sebagai Administrator kalau ada error permission.

## 1.6 Akun Telegram

Download Telegram di HP: https://telegram.org/
Bikin username — nanti dipake notifikasi bot.

---

# 2. Panduan Workshop Lengkap

## 2.1 Kenapa Bot Sinyal?

Lo ga perlu jadi programmer buat bikin signal bot.

**Cukup:**
- Bisa buka terminal
- Bisa copy-paste
- Mau nyobain

AI assistant (Hermes Agent) yang nanganin sisanya:
> Download template → jalanin → cron-in → sinyal masuk HP

Hasil akhirnya:
> Tiap X jam, bot analisa pasar, generate sinyal, kirim ke Telegram.
> Lo tinggal baca, eksekusi kalau cocok.

**⚠️ Penting:** Ini signal bot, bukan execution bot. Bot kita kasih sinyal beli/jual — lo sendiri yang eksekusi di exchange. Aman, ga konek API exchange.

## 2.2 Kenapa Hermes Agent?

- **Open source** — gratis, ga ada biaya langganan
- **Cron bawaan** — bot jalan otomatis tanpa server
- **Multi-provider** — bisa pake Claude, GPT, DeepSeek, bebas
- **Multi-platform** — Telegram, Discord, file, email

## 2.3 Install Hermes Agent

Buka terminal (CMD / PowerShell / Terminal Mac/Linux):

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Cek:
```bash
hermes doctor
```

## 2.4 Setup Provider — OpenRouter (Gratis)

```bash
hermes model
```

1. Pilih: **OpenRouter**
2. Paste API key yang udah di-copy tadi
3. Pilih model: **DeepSeek V3** (gratis, cepet, cukup buat workshop)

**Model gratis lainnya:**
| Model | Bagus buat |
|-------|-----------|
| DeepSeek V3 | Signal analisa, prompt umum |
| Qwen 2.5 72B | Coding sederhana |
| Gemini Flash | Gratis unlimited |

## 2.5 Jalanin Bot Template

Download `trading_bot_template.py` dari link workshop.

Jalanin:
```bash
python trading_bot_template.py
```

**Output yang diharapkan:**
```
TRADING SIGNAL — 25 Jul 13:30 WIB
========================================
Price: $4,075.70 (+1.71%)
Direction: 🟢 LONG | Confidence: 95%
Entry: $4,075.70
SL: $3,962.50 | TP: $4,113.20
R:R 1:1.67

Reasons:
  • RSI 66>50 bullish bias
  • EMA9>21 bullish
  • Price > BB mid
  • MACD+ bullish momentum

⚠️ AI-generated signal. Not financial advice. DYOR.
```

**Kalau bot silent (ga ada output)?** Itu normal. Bot punya cooldown 4 jam — ga akan generate sinyal kalau masih ada posisi aktif atau baru aja generate.

Cek history sinyal:
```bash
cat signals.json
```

## 2.6 Cron — Bot Jalan Otomatis

Manual `python trading_bot.py` tiap hari? Capek.

**Cron = bot jalan sendiri, lo tinggal terima hasil.**

```bash
hermes cron create 'every 4h' \
  --name "Sinyal Auto" \
  --prompt "Jalankan python trading_bot_template.py 2>&1. Kirim output apa adanya."
```

Cek cron:
```bash
hermes cron list
```

## 2.7 Kirim ke Telegram

```bash
hermes gateway setup
```

1. Pilih Telegram
2. Bikin bot lewat @BotFather di Telegram → dapetin token
3. Start bot di HP
4. Update cron biar deliver ke Telegram:

```bash
hermes cron update <job_id> --deliver telegram
```

Tiap 4 jam, sinyal masuk HP. Lo ga perlu buka laptop.

---

# 3. Trading Bot Template (Full Code)

File: `trading_bot_template.py`

```python
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
    ema = sum(prices[-period:]) / period
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
    """Upper band = overbought. Lower band = oversold."""
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

    # Cek cooldown
    if last_signal and last_signal.get("status") == "active":
        return None  # masih ada posisi aktif

    if last_signal:
        last_time = datetime.fromisoformat(last_signal["timestamp"])
        elapsed = (datetime.now(timezone.utc) - last_time).total_seconds() / 3600
        if elapsed < COOLDOWN_HRS:
            return None  # masih cooldown

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


# ─── Main Loop ───
def main():
    # 1. Ambil harga
    price = fetch_price()
    if not price:
        print("❌ Gagal ambil harga. Cek koneksi / API.")
        return

    bid = price["bid"]

    # 2. Load history
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

    # 4. Cek posisi aktif
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
        # Bot silent — normal
        pass


if __name__ == "__main__":
    main()
```

---

# 4. Cheatsheet Prompt — Modifikasi Bot

Template bot udah siap. Tapi kalau mau modifikasi, tanya Hermes Agent pake prompt di bawah. Tinggal copas → ganti sesuai kebutuhan → AI akan ubah kodenya.

## 4.1 Modifikasi Template

**Ganti aset (XAU → BTC):**
> Ganti fetch_price di trading_bot_template.py supaya ambil harga BTC/USD dari CoinGecko API. Pakai url https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd. Parse response JSON untuk dapetin harga.

**Ubah interval sinyal (cooldown):**
> Ubah COOLDOWN_HRS di trading_bot_template.py jadi 2 jam bukan 4 jam.

**Tambah indikator baru:**
> Tambah function calc_stochastic(prices, period=14) ke trading_bot_template.py. Stochastic oscillator: %K = (close - lowest low) / (highest high - lowest low) * 100. Output signal overbought >80, oversold <20.

**Edit SL/TP rasio:**
> Ubah perhitungan SL di trading_bot_template.py jadi 2x ATR, TP jadi 3x ATR.

**Tambah moving average cross sebagai filter:**
> Tambah filter di generate_signal(): pastikan EMA9 > EMA21 baru kasih sinyal LONG, kebalikannya buat SHORT.

**Ganti bahasa output ke Indonesia:**
> Ubah format_signal() di trading_bot_template.py — ganti semua tulisan ke Bahasa Indonesia. Contoh: 'Direction' → 'Arah', 'Confidence' → 'Keyakinan'.

## 4.2 Cron & Telegram

**Setup cron (bot jalan otomatis):**
> Bantu saya setup cron job Hermes Agent buat jalanin python trading_bot_template.py tiap 6 jam. Kirim output lengkap sinyal ke saya.

**Setup Telegram:**
> Bantu saya setup Hermes Gateway ke Telegram. Saya punya Bot Token dari @BotFather. Langkah-langkahnya?

## 4.3 Troubleshooting

Kalau ada error, tinggal paste error ke Hermes:
> Error ini: [paste error]. Tolong fix.

**Error umum:**
| Error | Solusi |
|-------|--------|
| ModuleNotFoundError: No module named 'requests' | `pip install requests` |
| SyntaxError | Ada typo di line X |
| Bot jalan tapi ga output | Cooldown masih active / silent mode |

## 4.4 Tanya Konsep Trading

Gunakan ini kapan aja:
- "Jelaskan RSI dalam trading dengan analogi sederhana"
- "Apa beda EMA sama SMA? Kapan pakai masing-masing?"
- "Kenapa SL/TP harus dihitung pakai ATR?"
- "Apa itu Bollinger Bands squeeze?"
- "Cara backtest sinyal trading tanpa modal?"
- "Apa indikator paling penting buat gold trading?"
- "Kenapa WR 60% lebih profit daripada WR 90%?"

---

# 5. Alur Cepat — Ringkasan

## Setup Provider (Step Detail)

**OpenRouter — Gratis:**
1. Buka https://openrouter.ai/keys
2. Login (Google/GitHub/email)
3. Klik "Create Key" → copy API key
4. `hermes model` → pilih OpenRouter → paste key → pilih DeepSeek V3

**Alternatif:**
- Gemini API → https://aistudio.google.com/apikey (60 req/menit gratis)
- Ollama local → `ollama pull llama3.2` (butuh RAM 8GB+)

## Quick Start (6 Langkah)

1. **Install Hermes Agent:**
   ```bash
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   ```

2. **Setup provider:**
   ```bash
   hermes model
   ```
   → OpenRouter → paste API key → DeepSeek V3

3. **Download template:**
   Dapatkan `trading_bot_template.py` dari link workshop

4. **Jalanin bot:**
   ```bash
   python trading_bot_template.py
   ```

5. **Cron otomatis:**
   ```bash
   hermes cron create 'every 6h' --name "Sinyal Saya" --prompt "Jalankan python trading_bot_template.py 2>&1"
   ```

6. **Telegram (opsional):**
   ```bash
   hermes gateway setup
   ```

**Selesai!** Bot sinyal lo udah jalan otomatis.

---

# 6. Tips & Best Practices

✅ **Mulai 1 aset** — XAU atau BTC, jangan semua
✅ **SL wajib** — jangan entry tanpa SL
✅ **Backtest** — pantau seminggu sebelum real trade
✅ **Cross-check** — AI bisa salah, cek chart manual
✅ **Konsisten** — 3 sinyal bagus > 20 sinyal random

❌ Jangan langsung trade real money
❌ Jangan over-trading (cron tiap jam = spam)
❌ Jangan percaya 100% ke AI — lo tetap bosnya

---

# 7. Resources

| Resource | Link |
|----------|------|
| Hermes Agent | https://hermes-agent.nousresearch.com |
| OpenRouter | https://openrouter.ai/keys |
| Python Download | https://www.python.org/downloads/ |
| VS Code | https://code.visualstudio.com/ |
| Telegram Bot | https://t.me/botfather |
| CoinGecko API (data harga gratis) | https://www.coingecko.com/en/api |

---

**FROM ZERO TO TRADING BOTS**
Workshop PINTU × Web3 Dev Bandung
25 Juli 2026 | Parla Cafe, Bandung

Instructor: Putra

"Ga perlu jadi programmer. Cukup prompt, download, cron, jalan."
