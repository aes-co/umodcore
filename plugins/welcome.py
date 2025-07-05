
# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
from utils.core import register_command, handle_error, eor
from utils.db import mongodb

def register_welcome(client: TelegramClient):
    @register_command(client, "setwelcome")
    @handle_error
    async def set_welcome(event):
        """Set a welcome message for a chat"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        args = event.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await mongodb.clear_welcome_message(event.chat_id)
            await eor(event, "✅ Pesan selamat datang dinonaktifkan.")
            return

        welcome_message = args[1]
        await mongodb.set_welcome_message(event.chat_id, welcome_message)
        await eor(event, f"✅ Pesan selamat datang berhasil diatur.")

    @client.on(events.ChatAction)
    @handle_error
    async def on_user_join(event):
        """Handle new user joining a chat"""
        if not mongodb.db or not event.user_joined:
            return

        welcome_message = await mongodb.get_welcome_message(event.chat_id)
        if not welcome_message:
            return

        user = await event.get_user()
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        message = welcome_message.format(mention=mention, chat_name=(await event.get_chat()).title)

        await event.reply(message)
