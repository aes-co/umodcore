# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram.types import Message
import logging

logger = logging.getLogger(__name__)

async def eor(message: Message, text: str):
    """Edit or reply the message with fallback."""
    try:
        if message.from_user and message.from_user.is_self:
            return await message.edit(text)
        return await message.reply(text)
    except Exception as e:
        logger.error(f"Error in eor function: {e}")
        # Jika terjadi kesalahan, Anda bisa mengirim pesan baru sebagai fallback
        return await message.reply("❌ Terjadi kesalahan saat mencoba mengedit atau membalas pesan.")
