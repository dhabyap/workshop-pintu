# FROM ZERO TO TRADING BOTS
## PINTU × Web3 Dev Bandung — 25 Juli 2026

---

## Slide 1 — Title
**FROM ZERO TO TRADING BOTS**
Buat Bot Sinyal Pertamamu — Dari Nol ke Telegram dalam 45 Menit
PINTU × Web3 Dev Bandung
Sabtu, 25 Juli 2026
Instructor: Putra

---

## Slide 2 — About Me
- Web developer sejak 2021 (Laravel, PHP, Web3)
- Crypto & trader
- Jalanin trading signal bot otomatis (XAU, crypto)
- Bot gue: XAU — udah jalan 24/7, generate sinyal tiap 4 jam

---

## Slide 3 — Agenda (45 Menit)
1. Install AI Assistant (5m)
2. Setup Provider (5m)
3. Dapetin Bot Template (5m)
4. Jalanin Bot + Lihat Sinyal (10m)
5. Auto-cron — Bot Jalan Sendiri (10m)
6. Kirim ke Telegram (5m)
7. Q&A (5m)

---

## Slide 4 — Kenapa Bot Sinyal? Kenapa Gampang?

Lo ga perlu jadi programmer buat bikin signal bot.

**Cukup:**
- Bisa buka terminal
- Bisa copy-paste
- Mau nyobain

AI assistant (Hermes Agent) yang nanganin sisanya:
- Download template → jalanin → cron-in → sinyal masuk HP

Hasil akhirnya:
> Tiap X jam, bot analisa pasar, generate sinyal, kirim ke Telegram.
> Lo tinggal baca, eksekusi kalau cocok.

---

## Slide 5 — Kenapa Hermes Agent?
- **Open source** — gratis
- **Cron bawaan** — bot jalan otomatis tanpa server
- **Multi-provider** — Claude, GPT, DeepSeek, bebas
- **Multi-platform** — Telegram, Discord, file

---

## Slide 6 — Install Hermes Agent

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Cek:
```bash
hermes doctor
```

**Windows:** Python 3.10+ harus udah terinstall.
Bantu temen sebelah kalau error.

---

## Slide 7 — Setup Provider (Gratis)

**Step 1 — Daftar OpenRouter**
Buka https://openrouter.ai/keys
Login (Google/GitHub/email)
Klik "Create Key" → Copy API key

**Step 2 — Setup Hermes**
```bash
hermes model
```
Pilih: OpenRouter → paste API key → pilih model

**Model gratis rekomendasi:**
| Model | Bagus buat |
|-------|-----------|
| DeepSeek V3 | Signal analisa, prompt umum |
| Qwen 2.5 72B | Coding sederhana |
| Gemini Flash | Gratis unlimited |

**Saran:** DeepSeek V3 — gratis, cepet, cukup buat workshop.

**Alternatif:**
- Ollama (local) — butuh download model 4-8GB
- Gemini API — 60 request/menit gratis
- GitHub Copilot — pakai akun GitHub

---

## Slide 8 — Template Bot Udah Siap
Template bot ada di link / QR code:

```
trading_bot_template.py — 230 baris
```

Isinya:
- Fetch harga dari Kitco (demo mode)
- RSI, EMA, MACD, Bollinger Bands, ATR
- Generate sinyal LONG/SHORT + SL/TP
- Simpan ke JSON
- Silent mode (ga spam)

**Ga perlu nulis kode. Tinggal download dan jalanin.**

---

## Slide 9 — Jalanin Bot

```bash
python trading_bot_template.py
```

Output:
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

⚠️ AI-generated signal. DYOR.
```

Bot juga simpan history di `signals.json` + `history.json`.

---

## Slide 10 — Kenapa Bot Diam?
Bot lo ga ngomong tiap detik.

- **Cooldown** — 4 jam jeda antar sinyal
- **Active guard** — gak generate kalau masih ada posisi aktif
- **Silent mode** — cuma output kalau ada sinyal BARU atau posisi CLOSED

Mau liat status kapan aja? Buka `signals.json` atau jalanin ulang bot.

---

## Slide 11 — LIVE DEMO: Bot XAU Saya

Tampilkan output real:
```
🪙 XAU SIGNAL — 21 Jul 23:25 WIB
Active: LONG entry $4,019 → P&L +1.41%
WR: 25% (1W/4L)
```

Ini bot gue — jalan 24/7, generate sinyal, kirim ke Telegram.
Gue ga pernah coding ulang. Template → cron → done.

---

## Slide 12 — Cron: Bot Jalan Otomatis

Manual `python trading_bot.py` tiap hari? Capek.

**Cron = bot jalan sendiri, lo tinggal terima hasil.**

```bash
hermes cron create 'every 4h' \
  --name "Sinyal XAU Auto" \
  --prompt "Jalankan python trading_bot_template.py 2>&1. Kirim output apa adanya."
```

---

## Slide 13 — Bonus: Kirim ke Telegram

```bash
hermes gateway setup
```

1. Pilih Telegram
2. Bikin bot lewat @BotFather → dapetin token
3. Start bot di HP

Update cron:
```bash
hermes cron update <job_id> \
  --deliver telegram
```

Tiap 4 jam, sinyal masuk HP. Lo ga perlu buka laptop.

---

## Slide 14 — HANDS-ON: Peserta Praktik (15m)

**Step 1 — Install**
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

**Step 2 — Download template**
(QR code / USB / link)

**Step 3 — Jalanin**
```bash
python trading_bot_template.py
```

**Step 4 — Cron**
```bash
hermes cron create 'every 8h' \
  --name "Sinyal Saya" \
  --prompt "Jalankan python trading_bot_template.py 2>&1"
```

**Selesai.** Bot sinyal lo udah jalan.

---

## Slide 15 — Tips & Best Practices
✅ **Mulai 1 aset** — XAU atau BTC, jangan semua
✅ **SL wajib** — jangan entry tanpa SL
✅ **Backtest** — pantau seminggu sebelum real trade
✅ **Cross-check** — AI bisa salah, cek chart manual
✅ **Konsisten** — 3 sinyal bagus > 20 sinyal random

❌ Jangan langsung trade real money
❌ Jangan over-trading (cron tiap jam = spam)
❌ Jangan percaya 100% ke AI — lo tetap bosnya

---

## Slide 16 — Live Bot Gue: Bukti Nyata
Tampilkan dashboard HTML (open `xau_dashboard.html` atau `xau_entry_reasons.html`)

"Ini bot gue — udah generate 5 sinyal, 1 win, 4 loss.
WR 25% tapi profit karena risk management (SL kecil, TP besar).
Bot tetap jalan walau loss. Yang penting konsisten."

---

## Slide 17 — Resources
- Hermes Agent: https://hermes-agent.nousresearch.com
- Template bot: [link / QR code]
- Cheatsheet prompt: [link / QR code]
- My bot dashboard: [link kalau ada]

---

## Slide 18 — Q&A
**Terima kasih!**

"Lo punya signal generator sendiri sekarang.
Ga perlu jadi programmer. Cukup prompt, download, cron, jalan."

@Putra | [Telegram / WA]
