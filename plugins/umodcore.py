# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import logging

from config import LOG_CHANNEL  # Pastikan LOG_CHANNEL diatur dengan benar
from utils.core import eor

logger = logging.getLogger(__name__)

# Pesan dan tombol yang akan digunakan
REPOMSG = """
🐾 **MODCORE USERBOT** 🐾

📦 Repo: [ModCore Userbot](https://github.com/aesneverhere/umodcore)
🧩 ModCore Bot: [Klik di sini](https://github.com/aesneverhere/modcore)
👑 Owner: @aesneverhere
"""

RP_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📦 Repo", url="https://github.com/aesneverhere/umodcore"),
        InlineKeyboardButton("🤖 ModCore Bot", url="https://github.com/aesneverhere/modcore")
    ],
    [
        InlineKeyboardButton("👤 Owner", url="https://t.me/aesneverhere")
    ]
])

MDCRSTRING = """✨ **Terima kasih telah menggunakan ModCore Userbot!**

🔧 Gunakan perintah `.help` atau `/help` untuk mulai.
📌 Jangan lupa cek repo dan dokumentasi ya!
"""

PHOTO_URL = "https://octodex.github.com/images/mona-whisper.gif"

def register_umodcore(app: Client):
    @app.on_message(filters.text & filters.regex(r"^\.repo$"))
    async def show_repo(client: Client, message: Message):
        try:
            await message.reply(REPOMSG, reply_markup=RP_BUTTONS)
        except Exception as e:
            logger.error(f"Error in /repo: {e}")
            await eor(message, "❌ Gagal menampilkan informasi repo.")

    @app.on_message(filters.text & filters.regex(r"^\.umodcore$"))
    async def show_intro(client: Client, message: Message):
        try:
            sent = await client.send_photo(
                chat_id=LOG_CHANNEL,
                photo=PHOTO_URL,
                caption=MDCRSTRING,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⚙️ Mulai >>", callback_data="init_modcore")]
                ])
            )
            if message.chat.id != LOG_CHANNEL:
                await message.reply(f"📍 Lihat hasilnya di [sini]({sent.link})", disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Error in /umodcore: {e}")
            await eor(message, "❌ Gagal mengirim pengenalan ModCore.")
