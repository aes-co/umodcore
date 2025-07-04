# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient
import os
import psutil
import platform
import logging
import speedtest
from datetime import datetime
from utils.core import (
    handle_error,
    eor,
    register_command,
    get_log_file,
    LOG_CHANNEL,
    get_uptime,
    format_duration,
    bot_state,
    get_command_count,
    is_admin
)

def get_system_info():
    """Get detailed system information"""
    try:
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return (
            f"💻 **System Information:**\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"CPU Usage: {cpu_percent}%\n"
            f"RAM: {memory.percent}% (Used: {memory.used // (1024*1024)}MB)\n"
            f"Disk: {disk.percent}% (Free: {disk.free // (1024*1024*1024)}GB)\n"
            f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"System Uptime: {format_duration(uptime.total_seconds())}\n"
        )
    except Exception as e:
        return f"Error getting system info: {str(e)}"

async def run_speedtest():
    """Run internet speed test"""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to MB/s
        upload_speed = st.upload() / 1_000_000  # Convert to MB/s
        ping = st.results.ping
        
        return (
            f"🚀 **Speed Test Results:**\n"
            f"Download: {download_speed:.2f} MB/s\n"
            f"Upload: {upload_speed:.2f} MB/s\n"
            f"Ping: {ping:.2f} ms"
        )
    except Exception as e:
        return f"Error running speedtest: {str(e)}"

def get_error_stats():
    """Get error statistics from log file"""
    try:
        error_count = 0
        warning_count = 0
        last_error = None
        last_error_time = None
        
        log_path = get_log_file()
        if log_path and os.path.exists(log_path):
            with open(log_path, 'r') as f:
                for line in f:
                    if 'ERROR' in line:
                        error_count += 1
                        last_error = line.strip()
                        # Try to extract timestamp
                        try:
                            last_error_time = line.split('[')[1].split(']')[0]
                        except:
                            pass
                    elif 'WARNING' in line:
                        warning_count += 1
        
        return (
            f"📊 **Error Statistics:**\n"
            f"Total Errors: {error_count}\n"
            f"Total Warnings: {warning_count}\n"
            f"Last Error: {last_error_time or 'N/A'}\n"
            f"Error Message: {last_error or 'No errors found'}"
        )
    except Exception as e:
        return f"Error getting statistics: {str(e)}"

def register_log(client: TelegramClient):
    @register_command(client, "log")
    @handle_error
    async def send_log(event):
        """Send message to log channel or send log file with statistics (Admin only)"""
        # Check if user is admin (owner or sudo)
        if not is_admin(event.sender_id):
            await eor(event, "⛔ Perintah ini hanya untuk admin bot!")
            return
            
        message_text = event.raw_text.split(maxsplit=1)[1] if len(event.raw_text.split()) > 1 else None
        
        if message_text:
            if LOG_CHANNEL:
                try:
                    await client.send_message(
                        LOG_CHANNEL,
                        f"📝 **Log dari {event.sender.first_name}:**\n\n{message_text}"
                    )
                    await eor(event, "✅ Pesan berhasil dikirim ke log channel!")
                except Exception as e:
                    await eor(event, f"❌ Gagal kirim ke log channel: {str(e)}")
            else:
                await eor(event, "❌ LOG_CHANNEL belum dikonfigurasi di .env file!")
        else:
            # Get all statistics
            stats = (
                f"🤖 **uModCore Status Report**\n\n"
                f"Bot Uptime: {get_uptime()}\n"
                f"Commands Executed: {get_command_count()}\n\n"
                f"{get_system_info()}\n\n"
                f"{get_error_stats()}\n\n"
            )
            
            # Add speedtest if requested
            if "-speed" in event.raw_text:
                await eor(event, f"{stats}\nRunning speedtest...")
                speed_stats = await run_speedtest()
                stats += f"\n{speed_stats}"
            
            # Send statistics and log file
            path = get_log_file()
            if path:
                await event.reply(
                    file=path,
                    caption=stats
                )
            else:
                await eor(event, stats + "\n🚫 Log file tidak ditemukan.")
