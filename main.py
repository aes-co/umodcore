# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

import asyncio
import os
from pyrogram import Client, idle, filters
from plugins.ping import register_ping
from plugins.me import register_me
from plugins.uinfo import register_uinfo
from plugins.reload import register_reload
from plugins.restart import register_restart
from plugins.alive import register_alive
from plugins.log import register_log
from plugins.afk import register_afk
from plugins.umodcore import register_umodcore
import config

app = Client(
    name="userbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING
)

register_ping(app)
register_me(app)
register_uinfo(app)
register_reload(app)
register_restart(app)
register_alive(app)
register_log(app)
register_afk(app)
register_umodcore(app)

notified = True

@app.on_message(filters.all)
async def notify_restart(_, msg):
    global notified
    if not notified and os.path.exists(".restart_chat_id"):
        try:
            with open(".restart_chat_id") as f:
                cid = int(f.read().strip())
            await app.send_message(cid, "✅ Userbot berhasil restart dan sudah aktif kembali.")
            os.remove(".restart_chat_id")
            notified = True
        except Exception as e:
            print("Gagal kirim notifikasi ke lokasi restart:", e)

async def main():
    await app.start()
    print("⚡️ Userbot ON, nyamar jadi manusia...")

    await idle()
    await app.stop()
    print("🥷 Userbot OFF, tarik diri...")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
