# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
from plugins import (
    ping, me, uinfo, reload, restart,
    alive, log, afk, umodcore, help,
    speedtest, start, auth, scheduler, customcmd, chatstats, automod, multilang, mediadl, inlinequery, reputation
)

# Load environment variables
load_dotenv()

# Get configuration from environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Initialize client with StringSession
client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

# Register plugins
ping.register_ping(client)
me.register_me(client)
uinfo.register_uinfo(client)
reload.register_reload(client)
restart.register_restart(client)
alive.register_alive(client)
log.register_log(client)
afk.register_afk(client)
umodcore.register_umodcore(client)
help.register_help(client)
speedtest.register_speedtest(client)
start.register_start(client)
auth.register_auth(client)  # Register auth plugin for sudo management
scheduler.register_scheduler(client)
customcmd.register_customcmd(client)
chatstats.register_chatstats(client)
automod.register_automod(client)
multilang.register_multilang(client)
mediadl.register_mediadl(client)
inlinequery.register_inlinequery(client)
reputation.register_reputation(client)

notified = True

@client.on(events.NewMessage)
async def notify_restart(event):
    global notified
    if not notified and os.path.exists(".restart_chat_id"):
        try:
            import time
            import psutil
            import platform
            
            with open(".restart_chat_id") as f:
                cid = int(f.read().strip())
            
            # Get restart duration
            restart_duration = "?"
            if os.path.exists(".restart_time"):
                with open(".restart_time") as f:
                    try:
                        restart_duration = f"{round(time.time() - float(f.read()), 2)}s"
                    except:
                        restart_duration = "Unknown"
            
            # Get system info
            cpu = platform.processor() or "Unknown"
            os_name = platform.system()
            os_ver = platform.release()
            mem = psutil.virtual_memory()
            ram_usage = f"{mem.used // (1024**2)} / {mem.total // (1024**2)} MB"
            python_ver = platform.python_version()
            
            # Calculate ping (simple method)
            start_time = time.time()
            await client.get_me()
            ping_ms = round((time.time() - start_time) * 1000, 2)
            
            restart_msg = (
                f"✅ **Userbot berhasil restart!**\n\n"
                f"⏱️ Restart Duration: `{restart_duration}`\n"
                f"🏓 Ping: `{ping_ms}ms`\n\n"
                f"💻 **System Info:**\n"
                f"OS: `{os_name} {os_ver}`\n"
                f"CPU: `{cpu}`\n"
                f"RAM: `{ram_usage}`\n"
                f"Python: `{python_ver}`\n\n"
                f"🚀 Bot siap digunakan!"
            )
            
            await client.send_message(cid, restart_msg)
            os.remove(".restart_chat_id")
            if os.path.exists(".restart_time"):
                os.remove(".restart_time")
            notified = True
        except Exception as e:
            print("Gagal kirim notifikasi ke lokasi restart:", e)

async def main():
    """Main function to start the userbot with optimizations for 30k+ groups"""
    print("🚀 Starting uModCore userbot...")
    print("⚡ Optimized for high-volume group management (30k+ groups)")
    
    # Start the client with optimizations
    await client.start()
    
    # Set client options for better performance
    client.parse_mode = 'md'  # Default parse mode
    
    print("✅ uModCore userbot is now running!")
    print("📊 Performance optimizations enabled")
    print("🔧 Message queue system active")
    print("📱 Ready to handle multiple groups simultaneously")
    
    # Keep the client running
    await client.run_until_disconnected()
    
    print("🥷 Userbot OFF, tarik diri...")

if __name__ == "__main__":
    asyncio.run(main())
