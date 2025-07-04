# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
from utils.core import (
    owner_only,
    handle_error,
    eor,
    register_command
)

def register_uinfo(client: TelegramClient):
    @register_command(client, "uinfo", owner_only=True)
    @handle_error
    async def uinfo(event):
        target = None
        if event.is_reply:
            r_msg = await event.get_reply_message()
            target = await r_msg.get_sender()
        else:
            target = await event.get_sender()

        text = (
            f"👤 <b>User Info</b>\n"
            f"🆔 ID       : <code>{target.id}</code>\n"
            f"🔗 Username : @{target.username if target.username else 'Tidak ada'}\n"
            f"📛 Nama     : {target.first_name} {target.last_name or ''}\n"
            f"🛡️ Premium  : {'✅ Ya' if getattr(target, 'premium', False) else '❌ Tidak'}\n"
            f"🤖 Bot      : {'Ya' if target.bot else 'Bukan'}"
        )
        await eor(event, text, parse_mode='html')
