# 🚀 ONE-CLICK DEPLOY: BTC SIGNAL BOT (Workshop Special)

Copy-paste seluruh prompt di bawah ini ke chat Hermes Agent. Hermes akan handle install, coding, eksekusi, sampai otomatisasi cron secara mandiri.

---

**PROMPT:**

"Saya sedang mengikuti workshop. Tolong deploy sistem Trading Signal Bot BTC/USD secara otonom:

1. **Install:** Pastikan library `requests` tersedia (`pip install requests`).
2. **Setup Code:** Buat file `btc_signal_bot.py`. Gunakan logika ini:
   - Ambil harga BTC live dari CoinGecko.
   - Simpan history harga ke `btc_history.json` (max 50 data).
   - Hitung indikator sederhana: Jika harga saat ini > rata-rata 5 data terakhir, sinyal = 'BULLISH', jika < rata-rata, sinyal = 'BEARISH'.
   - Tambahkan SL (2% di bawah entry) dan TP (5% di atas entry).
   - Simpan output final ke `btc_signals.json`.
3. **Demo Run:** Jalankan bot SEKARANG. Tampilkan output sinyal lengkap (Price, Direction, SL/TP) agar audiens bisa lihat data live.
4. **Otomatisasi:** Daftarkan cron job Hermes Agent dengan nama 'BTC-Auto-Signal' untuk jalan setiap 1 jam. Gunakan prompt: 'Jalankan python btc_signal_bot.py 2>&1'.
5. **Report:** Berikan ringkasan job ID cron dan cara saya mengecek file `btc_signals.json` nanti."

---

## Cara Verifikasi
Setelah Hermes selesai, lo bisa cek hasilnya dengan:
1. **Lihat Sinyal Terakhir:** `cat btc_signals.json`
2. **Cek Jadwal Otomatis:** `hermes cron list`
3. **Log Eksekusi:** `hermes cron logs <job_id>`
