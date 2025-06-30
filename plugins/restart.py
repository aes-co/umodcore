# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
import os
import sys
import asyncio
import time

def register_restart(app: Client):
    @app.on_message(filters.command("restart", prefixes=".") & filters.user(int(OWNER_ID)))
    async def restart_userbot(client: Client, message: Message):
        await message.reply_text("♻️ Restarting userbot... tunggu sebentar!")

        with open(".restart_chat_id", "w") as f:
            f.write(str(message.chat.id))

        with open(".restart_time", "w") as t:
            t.write(str(time.time()))

        await asyncio.sleep(1)
        os.execv(sys.executable, [sys.executable, "main.py"])
