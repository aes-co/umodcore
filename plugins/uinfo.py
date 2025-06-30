# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
import config

def register_uinfo(app: Client):
    @app.on_message(filters.command("uinfo", prefixes=".") & filters.user(int(config.OWNER_ID)))
    async def uinfo(client: Client, message: Message):
        target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        text = (
            f"👤 <b>User Info</b>\n"
            f"🆔 ID       : <code>{target.id}</code>\n"
            f"🔗 Username : @{target.username if target.username else 'Tidak ada'}\n"
            f"📛 Nama     : {target.first_name} {target.last_name or ''}\n"
            f"🛡️ Premium  : {'✅ Ya' if target.is_premium else '❌ Tidak'}\n"
            f"🤖 Bot      : {'Ya' if target.is_bot else 'Bukan'}"
        )
        await message.reply_text(text)
