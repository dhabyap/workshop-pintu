# 🚀 ONE-CLICK DEPLOY: BTC SIGNAL BOT (Workshop Special)

Copy-paste seluruh prompt di bawah ini ke chat Hermes Agent. Hermes akan handle install, coding, eksekusi, sampai otomatisasi cron secara mandiri.

---

**PROMPT:**

"Saya sedang mengikuti workshop. Tolong deploy sistem Trading Signal Bot BTC/USD secara otonom:

1. **Install:** Pastikan library `requests` tersedia (`pip install requests`).

2. **Setup Code:** Buat file `btc_signal_bot.py` di `~/`. Gunakan logika ini:
   - Ambil **history harga BTC 7 hari** dari CoinGecko (endpoint `/coins/bitcoin/market_chart?days=7`) biar data RSI langsung cukup.
   - Ambil harga BTC live dari CoinGecko setiap jalan.
   - Simpan history harga ke `btc_history.json` (max 100 data).
   - Hitung **MA 5** dan **RSI 14**.
   - Logika sinyal:
     - Jika MA5 arah = RSI arah → **CONFIDENCE HIGH**, entry ikut arah sama.
     - Jika MA5 ≠ RSI → **CONFIDENCE MEDIUM**, entry ikut MA5 (lebih dominan).
     - Tidak ada HOLD — bot selalu kasih sinyal trading.
   - RSI arah: >50 = bullish, <50 = bearish.
   - Confidence HIGH kalau MA5 & RSI aligned, MEDIUM kalau conflict.
   - Tambahkan SL (2%) dan TP (5%) dari entry price.

3. **Demo Run:** Jalankan bot SEKARANG. Tampilkan output profesional — timestamp, price, MA5, RSI14, sinyal LONG/SHORT, confidence, SL, TP, reason. Pastikan output bersih dan siap ditampilkan di layar workshop.

4. **Otomatisasi:** Daftarkan cron job Hermes Agent dengan nama 'BTC-Auto-Signal' untuk jalan setiap 1 jam. Pakai script wrapper `run_btc_bot.sh` yang execute `python btc_signal_bot.py`. Mode: no_agent=true, script=run_btc_bot.sh. Prompt tidak perlu — script langsung deliver output.

5. **Report:** Berikan ringkasan:
   - Job ID cron
   - Cara cek sinyal: `cat ~/btc_signals.json`
   - Cara baca sinyal: LONG = beli, SHORT = jual
   - Penjelasan: bot tidak pernah kasih HOLD, selalu siap entry dengan confidence HIGH/MEDIUM"

---

## Apa yang Baru di v2?

- ✅ **Data history 7 hari dari CoinGecko** — langsung dapet sinyal tanpa dummy
- ✅ **Tidak ada HOLD** — bot selalu kasih sinyal LONG/SHORT
- ✅ **RSI & MA5 alignment** — HIGH confidence kalau aligned, MEDIUM kalau conflict
- ✅ **Entry ikut MA5** — lebih dominan dari RSI kalau beda arah
- ✅ **100 candlesticks history** — data lebih akurat

## Cara Verifikasi

Setelah Hermes selesai:

```bash
# Lihat sinyal terakhir
cat ~/btc_signals.json

# Cek jadwal cron
hermes cron list

# History harga
cat ~/btc_history.json
```

## Cara Baca Sinyal

| Sinyal | Arah | SL | TP |
|--------|------|----|----|
| LONG 🟢 | Beli | Entry - 2% | Entry + 5% |
| SHORT 🔴 | Jual | Entry + 2% | Entry - 5% |

- **Confidence HIGH** → MA5 & RSI setuju — peluang bagus
- **Confidence MEDIUM** → MA5 & RSI beda arah — tetap gas ikut MA5, TP ketat
