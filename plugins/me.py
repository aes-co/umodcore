# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message

def register_me(app: Client):
    @app.on_message(filters.text & filters.regex(r"^\.me$"))
    async def whois(_, msg: Message):
        target = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user

        name = target.first_name or ""
        if target.last_name:
            name += " " + target.last_name
        username = f"@{target.username}" if target.username else "(no username)"

        await msg.reply(
            f"🕵️ Siapa nih?\n\n"
            f"🆔 ID: `{target.id}`\n"
            f"👤 Nama: {name}\n"
            f"🌐 Username: {username}\n"
            f"🤖 Tipe: {'Bot' if target.is_bot else 'User'}"
        )
