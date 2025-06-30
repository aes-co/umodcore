# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

AFK_DB = {}  # user_id: {since, reason}

def register_afk(app: Client):

    @app.on_message(filters.command("afk", prefixes="."))
    async def set_afk(client: Client, message: Message):
        user = message.from_user
        if not user:
            return
        reason = " ".join(message.command[1:]) if len(message.command) > 1 else "AFK tanpa alasan."
        AFK_DB[user.id] = {
            "since": datetime.now(),
            "reason": reason,
            "name": user.first_name
        }
        await message.reply(f"🙈 {user.first_name} sekarang AFK!\n📌 Alasan: {reason}")

    @app.on_message(filters.text)
    async def remove_afk(client: Client, message: Message):
        user = message.from_user
        if not user:
            return
        if user.id in AFK_DB:
            afk_data = AFK_DB.pop(user.id)
            duration = str(datetime.now() - afk_data["since"]).split(".")[0]
            await message.reply(
                f"✅ Welcome back, {user.first_name}!\n⏱️ AFK berakhir setelah: {duration}"
            )

    @app.on_message(filters.incoming & filters.group)
    async def reply_if_target_is_afk(client: Client, message: Message):
        # Cek reply
        if message.reply_to_message and message.reply_to_message.from_user:
            r_user = message.reply_to_message.from_user
            if r_user.id in AFK_DB:
                afk = AFK_DB[r_user.id]
                durasi = str(datetime.now() - afk["since"]).split(".")[0]
                await message.reply(
                    f"💤 {afk['name']} sedang AFK\n⏱️ Sejak: {durasi}\n📌 {afk['reason']}"
                )

        # Cek mention
        if message.entities:
            for e in message.entities:
                if e.type == "mention":
                    mentioned_username = message.text[e.offset:e.offset + e.length].lstrip("@")
                    try:
                        mentioned_user = await client.get_users(mentioned_username)
                        if mentioned_user.id in AFK_DB:
                            afk = AFK_DB[mentioned_user.id]
                            durasi = str(datetime.now() - afk["since"]).split(".")[0]
                            await message.reply(
                                f"💤 {afk['name']} sedang AFK\n⏱️ Sejak: {durasi}\n📌 {afk['reason']}"
                            )
                            break
                    except:
                        pass
