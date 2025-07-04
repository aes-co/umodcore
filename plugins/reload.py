# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from utils.core import (
    handle_error,
    eor,
    register_command,
    reload_plugins,
    is_admin
)

def register_reload(client: TelegramClient):
    @register_command(client, "reload")
    @handle_error
    async def handle_reload(event):
        """Reload all plugins (Admin only)"""
        # Check if user is admin (owner or sudo)
        if not is_admin(event.sender_id):
            await eor(event, "⛔ Perintah ini hanya untuk admin bot!")
            return
            
        status_msg = await eor(event, "🔄 Memuat ulang plugins...")
        successful, failed = reload_plugins(client)
        output = "🔄 Hasil Reload\n"
        if successful:
            output += "\n✅ Berhasil:\n" + "\n".join(f"• {x}" for x in successful)
        if failed:
            output += "\n\n❌ Gagal:\n" + "\n".join(f"• {x}" for x in failed)
        await status_msg.edit(output)
