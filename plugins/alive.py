# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
import platform
import psutil
import os
import time
from utils.core import (
    owner_only,
    handle_error,
    eor,
    get_uptime,
    register_command
)

def register_alive(client: TelegramClient):
    @register_command(client, "alive", owner_only=True)
    @handle_error
    async def alive(event):
        """Show bot status and system information"""
        restart_duration = "?"
        if os.path.exists(".restart_time"):
            with open(".restart_time") as f:
                try:
                    restart_duration = f"{round(time.time() - float(f.read()), 2)}s"
                except:
                    restart_duration = "Unknown"

        cpu = platform.processor() or "Unknown"
        os_name = platform.system()
        os_ver = platform.release()
        mem = psutil.virtual_memory()
        ram_usage = f"{mem.used // (1024**2)} / {mem.total // (1024**2)} MB"
        python_ver = platform.python_version()

        msg = (
            f"🤖 <b>Userbot Aktif!</b>\n"
            f"🟢 Status        : <code>Online</code>\n"
            f"🕰️ Uptime        : <code>{get_uptime()}</code>\n"
            f"⏱️ Waktu Restart : <code>{restart_duration}</code>\n\n"
            f"💻 OS            : <code>{os_name} {os_ver}</code>\n"
            f"🧠 CPU           : <code>{cpu}</code>\n"
            f"📦 RAM           : <code>{ram_usage}</code>\n"
            f"🐍 Python        : <code>{python_ver}</code>\n"
            f"📚 Telethon      : <code>{TelegramClient.__version__}</code>\n"
        )

        await eor(event, msg, parse_mode='html')
