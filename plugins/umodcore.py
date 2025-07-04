# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from telethon.tl.types import KeyboardButtonUrl
from utils.core import (
    eor,
    register_command,
    handle_error,
    delete_after,
    REPO_MSG,
    OWNER_USERNAME
)
import logging

logger = logging.getLogger(__name__)

def register_umodcore(client: TelegramClient):
    @register_command(client, "repo")
    @handle_error
    async def show_repo(event):
        try:
            # Add URL buttons (these work with userbots)
            buttons = [
                [KeyboardButtonUrl("📦 Repo", "https://github.com/aes-co/umodcore"),
                 KeyboardButtonUrl("🤖 ModCore Bot", "https://github.com/aes-co/modcore")],
                [KeyboardButtonUrl("👤 Owner", f"https://t.me/{OWNER_USERNAME}")]
            ]
            msg = await event.reply(REPO_MSG, buttons=buttons)
            await delete_after(msg, 45)
        except Exception as e:
            logger.error(f"Error in /repo: {e}")
            await eor(event, "❌ Gagal menampilkan informasi repo.")

    @register_command(client, "umodcore")
    @handle_error
    async def show_intro(event):
        try:
            intro_text = f"""✨ **Tentang uModCore Userbot**

🤖 **Apa itu uModCore?**
uModCore adalah userbot Telegram yang modular, cepat, dan ringan.
Dibangun menggunakan Telethon dengan fokus pada kemudahan penggunaan.

📋 **Fitur Utama:**
• Sistem plugin modular
• Auto-restart notification
• AFK mode dengan auto-reply
• System monitoring
• Error logging

🔧 **Quick Commands:**
• `.help` - Lihat semua command
• `.alive` - Cek status bot
• `.ping` - Test response time
• `.speedtest` - Test kecepatan

🔗 **Links:**
• Repo: https://github.com/aes-co/umodcore
• Owner: @{OWNER_USERNAME}

_Pesan ini akan terhapus otomatis dalam 45 detik_"""

            # Add URL buttons (these work with userbots)
            buttons = [
                [KeyboardButtonUrl("📦 Repo", "https://github.com/aes-co/umodcore"),
                 KeyboardButtonUrl("🤖 ModCore Bot", "https://github.com/aes-co/modcore")],
                [KeyboardButtonUrl("👤 Owner", f"https://t.me/{OWNER_USERNAME}")]
            ]
            
            msg = await event.reply(intro_text, buttons=buttons, parse_mode='md')
            await delete_after(msg, 45)
        except Exception as e:
            logger.error(f"Error in /umodcore: {e}")
            await eor(event, "❌ Gagal mengirim pengenalan ModCore.")
