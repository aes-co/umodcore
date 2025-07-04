# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
from utils.core import (
    handle_error,
    eor,
    register_command
)

def register_me(client: TelegramClient):
    @register_command(client, "me")
    @handle_error
    async def whois(event):
        target = None
        if event.is_reply:
            r_msg = await event.get_reply_message()
            target = await r_msg.get_sender()
        else:
            target = await event.get_sender()

        name = target.first_name or ""
        if target.last_name:
            name += " " + target.last_name
        username = f"@{target.username}" if target.username else "(no username)"

        text = (
            f"🕵️ Siapa nih?\n\n"
            f"🆔 ID: `{target.id}`\n"
            f"👤 Nama: {name}\n"
            f"🌐 Username: {username}\n"
            f"🤖 Tipe: {'Bot' if target.bot else 'User'}"
        )
        await eor(event, text)
