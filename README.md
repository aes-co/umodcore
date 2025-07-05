<p align="center">
  <img src="https://github.com/images/mona-whisper.gif" alt="uModCore Cat Logo" width="150"/>
</p>

<h1 align="center"><b>uModCore — Telegram Userbot</b></h1>

<p align="center">
  A modular, fast, and minimal Telegram Userbot built using Telethon.
</p>

<p align="center">
  <a href="https://github.com/aes-co/umodcore"><img src="https://img.shields.io/github/stars/aes-co/umodcore?style=flat-square&color=yellow" alt="Stars"/></a>
  <a href="https://github.com/aes-co/umodcore/fork"><img src="https://img.shields.io/github/forks/aes-co/umodcore?style=flat-square&color=orange" alt="Forks"/></a>
  <a href="https://github.com/aes-co/umodcore"><img src="https://img.shields.io/github/repo-size/aes-co/umodcore?style=flat-square&color=green" alt="Repo Size"/></a>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python Version"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square" alt="Maintained"/>
  <img src="https://img.shields.io/badge/good%20first%20issue-welcome-blueviolet?style=flat-square" alt="Good First Issue"/>
  <img src="https://img.shields.io/badge/hacktoberfest-accepted-orange?style=flat-square" alt="Hacktoberfest"/>
</p>

---

## 🧠 Overview

**uModCore** adalah userbot Telegram modular yang simple, powerful, dan ringan.  
Dibangun menggunakan Telethon, terinspirasi dari [Ultroid](https://github.com/TeamUltroid/Ultroid) dan pengembangan [ModCore Bot](https://github.com/aes-co/modcore).

---

## 🚀 Features

Perintah tersedia (pakai titik, bukan slash!):

- `.ping` — Cek latency
- `.dl` — Mengunduh media dari berbagai sumber
- `.me` — Info akun kamu
- `.uinfo` — Info user lain
- `.alive` — Status hidup
- `.afk` — Auto-reply AFK
- `.log` — Kirim pesan ke log group
- `.restart` — Restart bot + auto notify
- `.reload` — Reload plugin tanpa restart
- `.umodcore` — Tentang uModCore
- `.save` — Menyimpan catatan
- `.notes` — Menampilkan daftar catatan
- `.clear` — Menghapus catatan
- `.setwelcome` — Mengatur pesan selamat datang

---

## ⚙️ Setup

### 1. Clone Repo

```bash
git clone https://github.com/aes-co/umodcore.git
cd umodcore
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Generate Session

```bash
python generate_session.py
```

### 4. Konfigurasi

Salin dan isi `config_sample.py` ke `config.py`:

```python
API_ID = 12345678  # Ganti dengan API ID kamu
API_HASH = "your_api_hash_here"
SESSION_STRING = "your_session_string_here"

OWNER_ID = 123456789
OWNER_USERNAME = "your_username_here"
SOURCE_CODE = "https://github.com/aes-co/umodcore"
LOG_CHANNEL = -123456789
```

### 5. Jalankan Userbot

```bash
python main.py
```

---

## 📂 Plugin System

- Semua plugin disimpan di folder `plugins/`
- Plugin dimuat secara dinamis dari `main.py`
- Gunakan `.reload` untuk memuat ulang plugin saat runtime

---

## 🤝 Credits

### Core & Inspirasi

- **[Telethon](https://github.com/LonamiWebs/Telethon)** — Framework utama userbot ini.
- **[TeamUltroid](https://github.com/TeamUltroid)** — Inspirasi struktur modular dan arsitektur.
- **[aesneverhere](https://t.me/aesneverhere)** — Developer utama & pencipta ModCore/uModCore.

### Fitur Downloader

- **[mirror-leech-telegram-bot](https://github.com/anasty17/mirror-leech-telegram-bot)** — Basis logika downloader.
- **[Aria2](https://github.com/aria2/aria2)** — Engine download kuat untuk HTTP, torrent, dan magnet.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — Alat utama untuk ekstraksi video/audio.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 📊 Want to Contribute?

We welcome contributions from the community! 😍

- Found a bug? [Open an issue](https://github.com/aes-co/umodcore/issues)
- Got a feature idea? [Start a discussion](https://github.com/aes-co/umodcore/discussions)
- Want to improve code? Just **fork → commit → PR**

Looking for your first contribution? Check our [good first issues](https://github.com/aes-co/umodcore/labels/good%20first%20issue)!

Hacktoberfest participant? Your PRs here count too!

---

<p align="center">
  <i>Made with ❤️ by <a href="https://t.me/aesneverhere">@aes-co</a></i>
</p>
