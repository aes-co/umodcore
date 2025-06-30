# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import platform
import psutil
import time
import config
import os
import pyrogram

start_time = time.time()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def register_alive(app: Client):
    @app.on_message(filters.command("alive", prefixes=".") & filters.user(int(config.OWNER_ID)))
    async def alive(_, message: Message):
        uptime = format_uptime(time.time() - start_time)

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
        pyrogram_ver = pyrogram.__version__
        python_ver = platform.python_version()

        msg = (
            f"🤖 <b>Userbot Aktif!</b>\n"
            f"🟢 Status        : <code>Online</code>\n"
            f"🕰️ Uptime        : <code>{uptime}</code>\n"
            f"⏱️ Waktu Restart : <code>{restart_duration}</code>\n\n"
            f"💻 OS            : <code>{os_name} {os_ver}</code>\n"
            f"🧠 CPU           : <code>{cpu}</code>\n"
            f"📦 RAM           : <code>{ram_usage}</code>\n"
            f"🐍 Python        : <code>{python_ver}</code>\n"
            f"📚 Pyrogram      : <code>{pyrogram_ver}</code>\n"
        )

        await message.reply_text(msg, disable_web_page_preview=True)
