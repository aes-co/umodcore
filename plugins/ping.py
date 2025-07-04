# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
import time
from utils.core import (
    handle_error,
    eor,
    register_command
)

def register_ping(client: TelegramClient):
    @register_command(client, "ping")
    @handle_error
    async def ping(event):
        """Measure bot response time"""
        start = time.time()
        
        # Different responses for reply vs normal ping
        if event.is_reply:
            replied = await event.get_reply_message()
            user = await replied.get_sender()
            msg = f"🏓 Pong bang {user.first_name}!"
        else:
            msg = "🏓 Pong dari userbot, siapa manggil? 😎"
            
        # Send response and calculate latency
        m = await eor(event, msg)
        end = time.time()
        
        # Add latency info to response
        latency = (end - start) * 1000  # Convert to ms
        if m:  # Check if message was sent successfully
            try:
                await m.edit(f"{msg}\n⚡ Latency: {latency:.2f}ms")
            except Exception as e:
                # If edit fails, send new message
                await eor(event, f"{msg}\n⚡ Latency: {latency:.2f}ms")
        else:
            # If initial message failed, send simple response
            await eor(event, f"🏓 Pong!\n⚡ Latency: {latency:.2f}ms")
