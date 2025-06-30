# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
import os
import config

def register_log(app: Client):
    @app.on_message(filters.command("log", prefixes=".") & filters.user(int(config.OWNER_ID)))
    async def send_log(client: Client, message: Message):
        path = "error.log" if os.path.exists("error.log") else "log.txt"
        if os.path.exists(path):
            await message.reply_document(document=path, caption="📤 Ini log file kamu:")
        else:
            await message.reply_text("🚫 Log file tidak ditemukan.")
