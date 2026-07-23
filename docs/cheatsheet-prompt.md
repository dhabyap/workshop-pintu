# CHEATSHEET — Workshop Rakit Bot Sinyal
## PINTU × Web3 Dev Bandung | 25 Juli 2026

Template bot sudah tersedia di repository ini sebagai file `bot/trading_bot_template.py`.
Anda tidak perlu mendownload dari link luar — cukup gunakan file yang sudah ada di folder workshop Anda.

──────────────────────────────────────────────────
## CARA PAKAI TEMPLATE
──────────────────────────────────────────────────

1. Buka terminal di folder tempat Anda menyimpan file workshop.
2. Pastikan file `trading_bot_template.py` ada di folder `bot/`.
3. Jalankan bot:
   ```bash
   python bot/trading_bot_template.py
   ```

──────────────────────────────────────────────────
## MODIFIKASI TEMPLATE
──────────────────────────────────────────────────

Kalau mau modifikasi, tanya Hermes Agent pake prompt di bawah.
Tinggal copas → ganti sesuai kebutuhan → AI akan ubah kodenya.

**Ganti aset (misal: XAU → BTC)**
> "Ganti fetch_price di bot/trading_bot_template.py supaya ambil harga BTC/USD dari CoinGecko API. Pakai url https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd. Parse response JSON untuk dapetin harga."

**Ubah interval sinyal (cooldown)**
> "Ubah COOLDOWN_HRS di bot/trading_bot_template.py jadi 2 jam bukan 4 jam."

**Tambah indikator baru**
> "Tambah function calc_stochastic(prices, period=14) ke bot/trading_bot_template.py. Stochastic oscillator: %K = (close - lowest low) / (highest high - lowest low) * 100. Output signal overbought >80, oversold <20."

**Edit SL/TP rasio**
> "Ubah perhitungan SL di bot/trading_bot_template.py jadi 2x ATR, TP jadi 3x ATR."

**Tambah moving average cross sebagai filter**
> "Tambah filter di generate_signal(): pastikan EMA9 > EMA21 baru kasih sinyal LONG, kebalikannya buat SHORT."

**Ganti bahasa output ke Indonesia**
> "Ubah format_signal() di bot/trading_bot_template.py — ganti semua tulisan ke Bahasa Indonesia. Contoh: 'Direction' → 'Arah', 'Confidence' → 'Keyakinan'."

──────────────────────────────────────────────────
## CRON & TELEGRAM
──────────────────────────────────────────────────

**Setup cron (bot jalan otomatis)**
> "Bantu saya setup cron job Hermes Agent buat jalanin python bot/trading_bot_template.py tiap 6 jam. Kirim output lengkap sinyal ke saya."

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
## ALUR CEPAT WORKSHOP
──────────────────────────────────────────────────

1. Install Hermes Agent → `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
2. Setup provider → `hermes setup`
3. Masuk ke folder workshop.
4. Jalanin → `python bot/trading_bot_template.py`
5. Cron → `hermes cron create 'every 6h' --name "Sinyal Saya" --prompt "Jalankan python bot/trading_bot_template.py 2>&1"`
6. (Opsional) Setup Telegram → `hermes gateway setup`

Selesai! Bot sinyal lo udah jalan otomatis. 🎉
