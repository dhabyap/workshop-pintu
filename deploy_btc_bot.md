# 🚀 ONE-CLICK DEPLOY: BTC SIGNAL BOT (Workshop Special)

Copy-paste seluruh prompt di bawah ini ke chat Hermes Agent. Hermes akan handle install, coding, eksekusi, sampai otomatisasi cron secara mandiri.

---

**PROMPT:**

"Saya sedang mengikuti workshop. Tolong deploy sistem Trading Signal Bot BTC/USD secara otonom:

1. **Install:** Pastikan library `requests` tersedia (`pip install requests`).
2. **Setup Code:** Buat file `btc_signal_bot.py`. Gunakan logika ini:
   - Ambil harga BTC live dari CoinGecko setiap jalan.
   - Simpan history harga ke `btc_history.json` (max 50 data).
   - Hitung **MA 5** (sederhana) dan **RSI 14** untuk konfirmasi.
   - Logika sinyal:
     - Jika harga > MA 5 → **LONG** (BULLISH)
     - Jika harga < MA 5 → **SHORT** (BEARISH)
     - Jika harga = MA 5 → **HOLD** (NETRAL)
   - Konfirmasi RSI: RSI > 50 = bullish confirmation, RSI < 50 = bearish confirmation.
   - Tambahkan SL (2% di bawah entry) dan TP (5% di atas entry).
   - Output format profesional dengan timestamp, price, LONG/SHORT, RSI, MA, SL, TP, dan confidence level.
3. **Demo Run:** Jalankan bot SEKARANG. Tampilkan output dalam format tabel/block biar audiens bisa lihat data live. Inject dummy history biar langsung dapet sinyal real (bukan HOLD).
   - Contoh inject: `[64500, 64700, 64800, 64650, 64989]`
   - Jalankan 2-3x biar keliatan perubahan sinyal.
4. **Otomatisasi:** Daftarkan cron job Hermes Agent dengan nama 'BTC-Auto-Signal' untuk jalan setiap 1 jam. Pakai script wrapper `run_btc_bot.sh` yang execute `python btc_signal_bot.py` dan catat log. Prompt cron: 'Jalankan bash run_btc_bot.sh 2>&1'.
5. **Report:** Berikan ringkasan job ID cron, cara cek file `btc_signals.json`, dan cara baca sinyal (LONG = beli, SHORT = jual, HOLD = tunggu)."

---
