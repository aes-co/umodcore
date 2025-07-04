from telethon import events
from utils.core import register_command, eor, handle_error
import os
import aiohttp

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def register_mediadl(client):
    @register_command(client, "download")
    @handle_error
    async def download_media(event):
        """
        Download media from replied message or URL.
        Usage: .download (reply to media) or .download <url>
        """
        url = None
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            if reply and reply.media:
                file_path = await reply.download_media(file=DOWNLOAD_DIR)
                await eor(event, f"Media downloaded to {file_path}")
                return
            else:
                await eor(event, "Reply pesan tidak mengandung media.")
                return
        else:
            args = event.text.split(maxsplit=1)
            if len(args) < 2:
                await eor(event, "Usage: .download (reply to media) or .download <url>")
                return
            url = args[1]

        # Download from URL
        try:
            filename = url.split("/")[-1]
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open(file_path, "wb") as f:
                            f.write(await resp.read())
                        await eor(event, f"Media downloaded to {file_path}")
                    else:
                        await eor(event, f"Gagal mengunduh media, status: {resp.status}")
        except Exception as e:
            await eor(event, f"Error saat mengunduh media: {str(e)}")
