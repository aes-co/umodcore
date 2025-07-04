# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityMention
from datetime import datetime
from utils.core import (
    bot_state,
    eor,
    register_command,
    handle_error
)

def register_afk(client: TelegramClient):
    @register_command(client, "afk")
    @handle_error
    async def set_afk(event):
        user = await event.get_sender()
        if not user:
            return
        reason = event.raw_text.split(maxsplit=1)[1] if len(event.raw_text.split()) > 1 else "AFK tanpa alasan."
        bot_state.set_afk(user.id, user.first_name, reason)
        await eor(event, f"🙈 {user.first_name} sekarang AFK!\n📌 Alasan: {reason}")

    @client.on(events.NewMessage)
    @handle_error
    async def remove_afk(event):
        user = await event.get_sender()
        if not user:
            return
        
        # Don't remove AFK if it's a command (starts with .)
        if event.raw_text and event.raw_text.startswith('.'):
            return
            
        if bot_state.is_afk(user.id):
            afk_data = bot_state.remove_afk(user.id)
            duration = str(datetime.now() - afk_data["since"]).split(".")[0]
            await eor(event, f"✅ Welcome back, {user.first_name}!\n⏱️ AFK berakhir setelah: {duration}")

    @client.on(events.NewMessage(incoming=True))
    @handle_error
    async def reply_if_target_is_afk(event):
        # Check reply
        if event.is_reply:
            r_msg = await event.get_reply_message()
            r_user = await r_msg.get_sender()
            if bot_state.is_afk(r_user.id):
                afk = bot_state.get_afk_status(r_user.id)
                durasi = str(datetime.now() - afk["since"]).split(".")[0]
                await eor(
                    event,
                    f"💤 {afk['name']} sedang AFK\n⏱️ Sejak: {durasi}\n📌 {afk['reason']}"
                )
                return

        # Check mentions
        if event.entities:
            for e in event.entities:
                if isinstance(e, MessageEntityMention):
                    mentioned_username = event.raw_text[e.offset:e.offset + e.length].lstrip("@")
                    try:
                        mentioned_user = await client.get_entity(mentioned_username)
                        if bot_state.is_afk(mentioned_user.id):
                            afk = bot_state.get_afk_status(mentioned_user.id)
                            durasi = str(datetime.now() - afk["since"]).split(".")[0]
                            await eor(
                                event,
                                f"💤 {afk['name']} sedang AFK\n⏱️ Sejak: {durasi}\n📌 {afk['reason']}"
                            )
                            break
                    except:
                        pass
