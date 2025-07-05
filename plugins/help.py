# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from utils.core import (
    eor,
    register_command,
    handle_error,
    delete_after
)

def register_help(client: TelegramClient):
    @register_command(client, "help")
    @handle_error
    async def show_help(event):
        """Show available commands and help information"""
        help_text = """🤖 **UMODCORE USERBOT - BANTUAN**

**📋 Daftar Command Tersedia:**

**🔧 Public Commands (Semua user):**
• `.ping` - Test latency/response time
• `.me` - Info akun kamu sendiri
• `.uinfo` - Info user lain (reply/mention)
• `.afk [alasan]` - Set status AFK dengan auto-reply
• `.speedtest` - Test kecepatan internet
• `.dl <url>` - Unduh media dari URL dan unggah ke Telegram
• `.dlstatus` - Tampilkan status unduhan saat ini
• `.dlcancel <gid>` - Batalkan unduhan
• `.start` - Start message userbot
• `.lang <en/id>` - Ganti bahasa bot (multilang)

**⚙️ Admin Commands (Owner/Sudo only):**
• `.restart` - Restart userbot dengan notifikasi
• `.reload` - Reload semua plugin tanpa restart
• `.log [pesan]` - Kirim pesan ke log channel
• `.log -speed` - Log dengan speedtest
• `.auth @user` - Tambah sudo user (Owner only)
• `.deauth @user` - Hapus sudo user (Owner only)
• `.sudolist` - Lihat daftar sudo users (Owner only)
• `.setcookie` - Atur cookie untuk yt-dlp (Owner only)
• `.getcookie` - Dapatkan cookie yang tersimpan (Owner only)
• `.delcookie` - Hapus cookie yang tersimpan (Owner only)

**🗒️ Notes & Welcome:**
• `.save <nama> [teks]` - Simpan catatan
• `.notes` - Lihat daftar catatan
• `.clear <nama>` - Hapus catatan
• `.setwelcome [pesan]` - Atur pesan selamat datang

**📝 Fitur Multibahasa:**
• `.lang en` - Ganti bahasa bot ke English
• `.lang id` - Ganti bahasa bot ke Bahasa Indonesia
• File bahasa: `umodcore/lang/en.json` dan `umodcore/lang/id.json` bisa diedit sesuai kebutuhan.

**🗓️ Scheduler:**
• `.schedule <waktu> <pesan>` - Jadwalkan pesan (cth: `.schedule 10m Halo!`)
• `.cancelschedule <message_id>` - Batalkan pesan terjadwal

**🛠️ Custom Command:**
• `.addcmd <cmd> <response>` - Tambah custom command
• `.delcmd <cmd>` - Hapus custom command

**📊 Statistik & Reputation:**
• `.chatstats` - Statistik chat
• `.rep` - Lihat reputasi user (reply)
• `.uprep` - Upvote reputasi user (reply)

**🗂️ Download & Media:**
• `.dl <url>` - Download media dari url
• `.compress` - Kompres gambar (reply foto)
• `.tomp3` - Konversi video ke mp3 (reply video)

**📝 Cara Penggunaan:**
• Semua command menggunakan prefix titik (.)
• Public commands bisa digunakan semua user
• Admin commands hanya untuk owner dan sudo users
• Command `.alive` dihapus untuk keamanan

**🔗 Link Berguna:**
• Repo: https://github.com/aes-co/umodcore
• Issues: Laporkan bug di GitHub

_Pesan ini akan terhapus otomatis dalam 30 detik_
"""
        
        msg = await event.reply(help_text, parse_mode='md')
        # Auto delete after 30 seconds to avoid spam
        await delete_after(msg, 30)
