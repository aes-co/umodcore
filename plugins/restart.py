# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
import time
import os
from utils.core import (
    owner_only,
    handle_error,
    eor,
    register_command,
    restart_bot
)

def register_restart(client: TelegramClient):
    @register_command(client, "restart")
    @handle_error
    async def restart_userbot(event):
        """Restart userbot with notification (Admin only)"""
        # Check if user is admin (owner or sudo)
        from utils.core import is_admin
        if not is_admin(event.sender_id):
            await eor(event, "⛔ Perintah ini hanya untuk admin bot!")
            return
            
        msg = await eor(event, "♻️ Restarting userbot... tunggu sebentar!")
        
        # Save restart time
        with open(".restart_time", "w") as f:
            f.write(str(time.time()))
            
        # Save chat ID for notification after restart
        with open(".restart_chat_id", "w") as f:
            f.write(str(event.chat_id))
            
        await restart_bot(event)
