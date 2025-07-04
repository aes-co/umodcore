from telethon import events
from utils.core import register_command, eor, handle_error, is_admin
import re

# List of banned words (example)
BANNED_WORDS = ["spamword1", "badword", "anotherbadword"]

def register_automod(client):
    @client.on(events.NewMessage)
    async def auto_moderate(event):
        if event.is_private:
            return  # Skip private chats

        text = event.raw_text.lower()
        for banned_word in BANNED_WORDS:
            if banned_word in text:
                try:
                    await event.delete()
                    await event.respond("🚫 Pesan mengandung kata terlarang dan telah dihapus.")
                except:
                    pass
                break

    @register_command(client, "setbanned")
    @handle_error
    async def set_banned_words(event):
        """
        Set banned words list (Admin only).
        Usage: .setbanned word1 word2 word3
        """
        if not is_admin(event.sender_id):
            await eor(event, "⛔ Perintah ini hanya untuk admin bot!")
            return

        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "Usage: .setbanned word1 word2 ...")
            return

        global BANNED_WORDS
        BANNED_WORDS = args[1].lower().split()
        await eor(event, f"Daftar kata terlarang diperbarui: {', '.join(BANNED_WORDS)}")
