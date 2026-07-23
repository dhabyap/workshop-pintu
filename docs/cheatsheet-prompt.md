# CHEATSHEET — Workshop Rakit Bot Sinyal
## PINTU × Web3 Dev Bandung | 25 Juli 2026

Template bot udah siap. Tapi kalau mau modifikasi, tanya Hermes Agent pake prompt di bawah.
Tinggal copas → ganti sesuai kebutuhan → AI akan ubah kodenya.

──────────────────────────────────────────────────
## MODIFIKASI TEMPLATE
──────────────────────────────────────────────────

**Ganti aset (misal: XAU → BTC)**
> "Ganti fetch_price di trading_bot_template.py supaya ambil harga BTC/USD dari CoinGecko API. Pakai url https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd. Parse response JSON untuk dapetin harga."

**Ubah interval sinyal (cooldown)**
> "Ubah COOLDOWN_HRS di trading_bot_template.py jadi 2 jam bukan 4 jam."

**Tambah indikator baru**
> "Tambah function calc_stochastic(prices, period=14) ke trading_bot_template.py. Stochastic oscillator: %K = (close - lowest low) / (highest high - lowest low) * 100. Output signal overbought >80, oversold <20."

**Edit SL/TP rasio**
> "Ubah perhitungan SL di trading_bot_template.py jadi 2x ATR, TP jadi 3x ATR."

**Tambah moving average cross sebagai filter**
> "Tambah filter di generate_signal(): pastikan EMA9 > EMA21 baru kasih sinyal LONG, kebalikannya buat SHORT."

**Ganti bahasa output ke Indonesia**
> "Ubah format_signal() di trading_bot_template.py — ganti semua tulisan ke Bahasa Indonesia. Contoh: 'Direction' → 'Arah', 'Confidence' → 'Keyakinan'."

──────────────────────────────────────────────────
## CRON & TELEGRAM
──────────────────────────────────────────────────

**Setup cron (bot jalan otomatis)**
> "Bantu saya setup cron job Hermes Agent buat jalanin python trading_bot_template.py tiap 6 jam. Kirim output lengkap sinyal ke saya."

**Setup Telegram**
> "Bantu saya setup Hermes Gateway ke Telegram. Saya punya Bot Token dari @BotFather. Langkah-langkahnya?"

──────────────────────────────────────────────────
## TROUBLESHOOTING
──────────────────────────────────────────────────

Kalau ada error, tinggal paste error ke Hermes:
> "Error ini: [paste error]. Tolong fix."

Contoh error umum:
- "ModuleNotFoundError: No module named 'requests'" → "Install requests: pip install requests"
- "SyntaxError" → "Ada typo di line X"
- Bot jalan tapi ga output → "Bot cooldown masih active atau lagi silent mode"

──────────────────────────────────────────────────
## TANYA KONSEP (Bonus)
──────────────────────────────────────────────────

Gunakan ini kapan aja selama workshop:

- "Jelaskan RSI dalam trading dengan analogi sederhana"
- "Apa beda EMA sama SMA? Kapan pakai masing-masing?"
- "Kenapa SL/TP harus dihitung pakai ATR?"
- "Apa itu Bollinger Bands squeeze?"
- "Cara backtest sinyal trading tanpa modal?"
- "Apa indikator paling penting buat gold trading?"
- "Kenapa WR 60% lebih profit daripada WR 90%?"

──────────────────────────────────────────────────
## ALUR CEPAT WORKSHOP
──────────────────────────────────────────────────

1. Install Hermes Agent → `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
2. Setup provider → `hermes setup`
3. Download template `trading_bot_template.py`
4. Jalanin → `python trading_bot_template.py`
5. Cron → `hermes cron create 'every 6h' --name "Sinyal Saya" --prompt "Jalankan python trading_bot_template.py 2>&1"`
6. (Opsional) Setup Telegram → `hermes gateway setup`

Selesai! Bot sinyal lo udah jalan otomatis. 🎉
