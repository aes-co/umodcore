# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
import time
import os
from utils.core import (
    owner_only,
    handle_error,
    eor,
    register_command,
    restart_bot,
    format_duration
)
from utils.db import mongodb

def register_restart(client: TelegramClient):
    @register_command(client, "restart")
    @handle_error
    async def restart_userbot(event):
        """Restart userbot with notification (Admin only)"""
        from utils.core import is_admin
        if not is_admin(event.sender_id):
            await eor(event, "⛔ Perintah ini hanya untuk admin bot!")
            return
            
        msg = await eor(event, "♻️ Restarting userbot... tunggu sebentar!")
        
        # Save restart info to database
        await mongodb.set_restart_info(event.chat_id, time.time())
            
        await restart_bot(event)

    @client.on(events.NewMessage(outgoing=True, incoming=True))
    async def check_restart_notification(event):
        if not mongodb.db:
            return

        restart_info = await mongodb.get_restart_info()
        if restart_info:
            chat_id = restart_info["chat_id"]
            restart_timestamp = restart_info["timestamp"]

            # Only send notification if the message is in the restart chat
            if event.chat_id == chat_id:
                try:
                    import psutil
                    import platform

                    restart_duration = format_duration(time.time() - restart_timestamp)

                    # Get system info
                    cpu = platform.processor() or "Unknown"
                    os_name = platform.system()
                    os_ver = platform.release()
                    mem = psutil.virtual_memory()
                    ram_usage = f"{mem.used // (1024**2)} / {mem.total // (1024**2)} MB"
                    python_ver = platform.python_version()

                    # Calculate ping (simple method)
                    start_time = time.time()
                    await client.get_me()
                    ping_ms = round((time.time() - start_time) * 1000, 2)

                    restart_msg = (
                        f"✅ **Userbot berhasil restart!**\n\n"
                        f"⏱️ Restart Duration: `{restart_duration}`\n"
                        f"🏓 Ping: `{ping_ms}ms`\n\n"
                        f"💻 **System Info:**\n"
                        f"OS: `{os_name} {os_ver}`\n"
                        f"CPU: `{cpu}`\n"
                        f"RAM: `{ram_usage}`\n"
                        f"Python: `{python_ver}`\n\n"
                        f"🚀 Bot siap digunakan!"
                    )

                    await client.send_message(chat_id, restart_msg)
                except Exception as e:
                    print(f"Gagal kirim notifikasi ke lokasi restart: {e}")
