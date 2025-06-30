# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
import time

def register_ping(app: Client):
    @app.on_message(filters.text & filters.reply & filters.regex(r"^\.ping$"))
    async def ping_reply(_, msg: Message):
        user = msg.reply_to_message.from_user
        await msg.reply(f"🏓 Pong bang {user.first_name}!")

    @app.on_message(filters.text & filters.regex(r"^\.ping$"))
    async def ping_normal(_, msg: Message):
        await msg.reply(f"🏓 Pong dari userbot, siapa manggil? 😎")
