<p align="center">
  <img src="https://github.com/images/mona-whisper.gif" alt="uModCore Cat Logo" width="150"/>
</p>

<h1 align="center">
  <b>uModCore - UserBot</b>
</h1>

<p align="center">
  A modular, fast and minimal Telegram Userbot built using Pyrogram.
</p>

<p align="center">
  <a href="https://github.com/aeswnh/ummodcore"><img src="https://img.shields.io/github/stars/aeswnh/ummodcore?style=flat-square&color=yellow" alt="Stars"/></a>
  <a href="https://github.com/aeswnh/ummodcore/fork"><img src="https://img.shields.io/github/forks/aeswnh/ummodcore?style=flat-square&color=orange" alt="Forks"/></a>
  <a href="https://github.com/aeswnh/ummodcore"><img src="https://img.shields.io/github/repo-size/aeswnh/ummodcore?style=flat-square&color=green" alt="Repo Size"/></a>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square" alt="Maintained"/>
  <img src="https://img.shields.io/badge/good%20first%20issue-welcome-blueviolet?style=flat-square" alt="Good First Issue"/>
  <img src="https://img.shields.io/badge/hacktoberfest-accepted-orange?style=flat-square" alt="Hacktoberfest"/>
</p>

---

## 🧠 Overview

`uModCore` adalah userbot Telegram modular yang simple, powerful, dan ringan.
Dibangun menggunakan Pyrogram, terinspirasi dari [Ultroid](https://github.com/TeamUltroid/Ultroid) dan pengembangan [ModCore Bot](https://github.com/aeswnh/modcore).

---

## 🚀 Features

Berikut command yang tersedia (pakai titik, bukan slash!):

* `.ping` — Cek latency
* `.me` — Info akunmu
* `.uinfo` — Info user lain
* `.alive` — Status hidup
* `.afk` — Auto reply AFK
* `.log` — Kirim pesan ke log group
* `.restart` — Restart bot + auto notify
* `.reload` — Reload plugin tanpa restart
* `.umodcore` — Tentang uModCore

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/aeswnh/ummodcore.git
cd ummodcore
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Generate session

```bash
python generate_session.py
```

### 4. Konfigurasi

Salin dan isi `config_sample.py` → `config.py`:

```python
# Sample Configuration for uModCore Userbot

API_ID = 12345678  # Ganti dengan API ID kamu
API_HASH = "your_api_hash_here"
SESSION_STRING = "your_session_string_here"

OWNER_ID = 123456789 
OWNER_USERNAME = "your_username_here"
SOURCE_CODE = "https://github.com/aeswnh/ummodcore"
LOG_CHANNEL = -123456789
```

### 5. Jalankan userbot

```bash
python main.py
```

---

## 📂 Plugin System

* Semua plugin tinggal taruh di folder `plugins/` dan daftarkan di `main.py`
* Bisa reload runtime pakai `.reload` tanpa restart

---

## 🤝 Credits

* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [TeamUltroid](https://github.com/TeamUltroid) — for structure inspiration
* [aesneverhere](https://github.com/aesneverhere) — original creator of ModCore & uModCore

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📊 Want to Contribute?

We welcome contributions from the community! 🤩

* Found a bug? [Open an issue](https://github.com/aeswnh/ummodcore/issues).
* Got a feature idea? [Start a discussion](https://github.com/aeswnh/ummodcore/discussions).
* Want to improve code? Just fork the repo, push changes, and make a PR!

Your contributions are appreciated and will be credited ✨

Looking for your first contribution? Check out our [good first issues](https://github.com/aeswnh/ummodcore/labels/good%20first%20issue)!

Participating in Hacktoberfest? Your PRs here count!

---

<p align="center">Made with 💖 by <a href="https://t.me/aesneverhere">@aesneverhere</a></p>