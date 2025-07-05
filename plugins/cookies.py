from telethon import TelegramClient, events
from utils.core import register_command, handle_error, eor, owner_only
from utils.db import mongodb
import os


def register_cookies(client: TelegramClient):
    @register_command(client, "setcookie", owner_only=True)
    @handle_error
    async def set_cookie_command(event):
        """Set cookies for yt-dlp from a replied .txt file (Owner only)"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        reply_message = await event.get_reply_message()
        if not reply_message or not reply_message.file or not reply_message.file.name.endswith(".txt"):
            await eor(event, "❓ Balas file `.txt` yang berisi cookie Anda.")
            return

        try:
            # Download the file
            cookie_file_path = await reply_message.download_media(file="./temp_cookie.txt")
            with open(cookie_file_path, "r") as f:
                cookies_content = f.read()
            os.remove(cookie_file_path) # Clean up the downloaded file

            await mongodb.set_user_cookies(event.sender_id, cookies_content)
            await eor(event, "✅ Cookie berhasil disimpan.")
        except Exception as e:
            await eor(event, f"❌ Gagal menyimpan cookie: {str(e)}")

    @register_command(client, "getcookie", owner_only=True)
    @handle_error
    async def get_cookie_command(event):
        """Get stored cookies (Owner only)"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        cookies_content = await mongodb.get_user_cookies(event.sender_id)
        if cookies_content:
            # Send as a file for security and formatting
            with open("user_cookies.txt", "w") as f:
                f.write(cookies_content)
            await client.send_file(event.chat_id, "user_cookies.txt", caption="Cookie Anda:", reply_to=event.id)
            os.remove("user_cookies.txt")
        else:
            await eor(event, "ℹ️ Tidak ada cookie yang tersimpan.")

    @register_command(client, "delcookie", owner_only=True)
    @handle_error
    async def delete_cookie_command(event):
        """Delete stored cookies (Owner only)"""
        if not mongodb.db:
            await eor(event, "❌ MongoDB tidak terhubung.")
            return

        await mongodb.delete_user_cookies(event.sender_id)
        await eor(event, "✅ Cookie berhasil dihapus.")
