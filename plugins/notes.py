# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
from utils.core import register_command, handle_error, eor
from utils.db import mongodb

def register_notes(client: TelegramClient):
    @register_command(client, "save")
    @handle_error
    async def save_note(event):
        """Save a note"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        args = event.raw_text.split(maxsplit=2)
        if len(args) < 2:
            await eor(event, "❓ **Penggunaan:** `.save <nama_catatan> [balas ke pesan atau berikan teks]`")
            return

        note_name = args[1]
        reply_message = await event.get_reply_message()

        if len(args) > 2:
            note_content = args[2]
            await mongodb.db.notes.update_one(
                {"chat_id": event.chat_id, "note_name": note_name},
                {"$set": {"content": note_content, "type": "text"}},
                upsert=True
            )
        elif reply_message:
            if reply_message.text:
                note_content = reply_message.text
                await mongodb.db.notes.update_one(
                    {"chat_id": event.chat_id, "note_name": note_name},
                    {"$set": {"content": note_content, "type": "text"}},
                    upsert=True
                )
            else:
                await eor(event, "❌ Pesan yang dibalas harus berupa teks.")
                return
        else:
            await eor(event, "❓ **Penggunaan:** `.save <nama_catatan> [balas ke pesan atau berikan teks]`")
            return

        await eor(event, f"✅ Catatan `{note_name}` berhasil disimpan.")

    @register_command(client, "notes")
    @handle_error
    async def get_notes(event):
        """Get all notes in a chat"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        cursor = mongodb.db.notes.find({"chat_id": event.chat_id})
        notes = await cursor.to_list(length=100)

        if not notes:
            await eor(event, "ℹ️ Tidak ada catatan yang tersimpan di chat ini.")
            return

        note_list = "\n".join([f"- `{note['note_name']}`" for note in notes])
        await eor(event, f"**Daftar Catatan:**\n{note_list}")

    @register_command(client, "clear")
    @handle_error
    async def clear_note(event):
        """Clear a note"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        args = event.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "❓ **Penggunaan:** `.clear <nama_catatan>`")
            return

        note_name = args[1]
        result = await mongodb.db.notes.delete_one({"chat_id": event.chat_id, "note_name": note_name})

        if result.deleted_count > 0:
            await eor(event, f"✅ Catatan `{note_name}` berhasil dihapus.")
        else:
            await eor(event, f"❌ Catatan `{note_name}` tidak ditemukan.")

    @client.on(events.NewMessage(pattern=r"^#(\S+)"))
    @handle_error
    async def on_note_call(event):
        """Handle note calls"""
        if not mongodb.db:
            return

        note_name = event.pattern_match.group(1)
        note = await mongodb.db.notes.find_one({"chat_id": event.chat_id, "note_name": note_name})

        if note:
            await event.reply(note["content"])
