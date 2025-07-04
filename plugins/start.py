# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from telethon.tl.types import KeyboardButtonUrl
from utils.core import (
    eor,
    register_command,
    handle_error,
    delete_after,
    OWNER_USERNAME
)

def register_start(client: TelegramClient):
    @register_command(client, "start")
    @handle_error
    async def start_message(event):
        """Show start/welcome message"""
        start_text = f"""🤖 **Selamat datang di uModCore Userbot!**

✨ **Userbot Telegram yang powerful dan modular**

**🚀 Features:**
• Modular plugin system
• Fast & lightweight
• Easy to customize
• Built with Telethon

**📋 Quick Commands:**
• `.help` - Lihat semua command
• `.alive` - Cek status bot
• `.ping` - Test response time
• `.umodcore` - Info tentang bot
• `.speedtest` - Test kecepatan internet

**🔧 Admin Commands:**
• `.restart` - Restart bot
• `.reload` - Reload plugins
• `.log` - System logs

**💡 Tips:**
Gunakan `.help` untuk melihat daftar lengkap command yang tersedia!

**🔗 Useful Links:**
• Repo: https://github.com/aes-co/umodcore
• Owner: @{OWNER_USERNAME}

_Pesan ini akan terhapus otomatis dalam 45 detik_"""
        
        # Add URL buttons (these work with userbots)
        buttons = [
            [KeyboardButtonUrl("📦 Repo", "https://github.com/aes-co/umodcore"),
             KeyboardButtonUrl("🤖 ModCore Bot", "https://github.com/aes-co/modcore")],
            [KeyboardButtonUrl("👤 Owner", f"https://t.me/{OWNER_USERNAME}")]
        ]
        
        msg = await event.reply(start_text, buttons=buttons, parse_mode='md')
        # Auto delete after 45 seconds
        await delete_after(msg, 45)
