# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
import speedtest
from utils.core import (
    eor,
    register_command,
    handle_error,
    delete_after
)

def register_speedtest(client: TelegramClient):
    @register_command(client, "speedtest")
    @handle_error
    async def run_speedtest(event):
        """Test internet connection speed"""
        progress_msg = await eor(event, "🔄 **Menjalankan Speed Test...**\n\n0% ▒▒▒▒▒▒▒▒▒▒")
        
        try:
            test = speedtest.Speedtest()
            
            # Get best server
            await progress_msg.edit("🔄 **Menjalankan Speed Test...**\n\n20% ██▒▒▒▒▒▒▒▒")
            test.get_best_server()
            
            # Test download speed
            await progress_msg.edit("🔄 **Menjalankan Speed Test...**\n\n40% ████▒▒▒▒▒▒")
            download_speed = test.download() / 1_000_000  # Convert to MB/s
            
            # Test upload speed
            await progress_msg.edit("🔄 **Menjalankan Speed Test...**\n\n60% ██████▒▒▒▒")
            upload_speed = test.upload() / 1_000_000  # Convert to MB/s
            
            # Get ping
            await progress_msg.edit("🔄 **Menjalankan Speed Test...**\n\n80% ████████▒▒")
            ping = test.results.ping
            
            # Get server info
            server = test.results.server
            
            # Format results
            result = (
                f"🚀 **Speedtest Results**\n\n"
                f"**🌐 Server:**\n"
                f"- Name: `{server['host']}`\n"
                f"- Country: `{server['country']}`\n"
                f"- Sponsor: `{server['sponsor']}`\n\n"
                f"**📊 Speed:**\n"
                f"- Download: `{download_speed:.2f} MB/s`\n"
                f"- Upload: `{upload_speed:.2f} MB/s`\n"
                f"- Ping: `{ping:.2f} ms`\n\n"
                f"_Pesan ini akan terhapus otomatis dalam 60 detik_"
            )
            
            await progress_msg.edit(result)
            # Auto delete after 60 seconds
            await delete_after(progress_msg, 60)
            
        except Exception as e:
            await progress_msg.edit(f"❌ **Error running speedtest:**\n`{str(e)}`")
