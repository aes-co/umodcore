# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID
import importlib
import os
import sys

def register_reload(app: Client):
    @app.on_message(filters.command("reload", prefixes=".") & filters.user(int(OWNER_ID)))
    async def handle_reload(client, message: Message):
        folder = "plugins"
        sukses = []
        gagal = []

        for file in os.listdir(folder):
            if file.endswith(".py"):
                modname = f"{folder}.{file[:-3]}"
                try:
                    if modname in sys.modules:
                        importlib.reload(sys.modules[modname])
                    else:
                        importlib.import_module(modname)
                    sukses.append(file)
                except Exception as e:
                    gagal.append(f"{file} → {e}")

        output = "🔄 Reload Result\n"
        if sukses:
            output += "\n✅ Berhasil:\n" + "\n".join(f"• {x}" for x in sukses)
        if gagal:
            output += "\n\n❌ Gagal:\n" + "\n".join(f"• {x}" for x in gagal)

        await message.reply_text(output)
