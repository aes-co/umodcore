import asyncio
import os
import re
import time
import yt_dlp
from aioaria2 import Aria2WebsocketClient
from telethon.tl.types import Message
from utils.core import eor
from concurrent.futures import ThreadPoolExecutor

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

executor = ThreadPoolExecutor(max_workers=5)

class Aria2Downloader:
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if self.client is None or self.client.closed:
            self.client = await Aria2WebsocketClient.new("ws://localhost:6800/jsonrpc")
        return self.client

    async def add_download(self, link):
        client = await self._get_client()
        gid = await client.addUri([link], {'dir': DOWNLOAD_DIR})
        return gid

    async def get_status(self, gid=None):
        client = await self._get_client()
        if gid:
            return await client.tellStatus(gid)
        else:
            global_stat = await client.getGlobalStat()
            active = await client.tellActive()
            waiting = await client.tellWaiting(0, 1000)
            stopped = await client.tellStopped(0, 1000)
            return {'global': global_stat, 'active': active, 'waiting': waiting, 'stopped': stopped}

    async def cancel_download(self, gid):
        client = await self._get_client()
        return await client.forceRemove(gid)

    async def close(self):
        if self.client:
            await self.client.close()

aria2_downloader = Aria2Downloader()

async def get_link_type(link):
    if re.match(r'magnet:\?xt=urn:btih:[a-zA-Z0-9]*', link):
        return 'magnet'
    elif re.match(r'.*\.torrent', link):
        return 'torrent'
    else:
        ydl = yt_dlp.YoutubeDL({'quiet': True})
        try:
            info = ydl.extract_info(link, download=False)
            if info:
                return 'youtube-dl'
        except:
            pass
        return 'direct'

async def handle_download(link, message):
    link_type = await get_link_type(link)

    if link_type in ['magnet', 'torrent', 'direct']:
        gid = await aria2_downloader.add_download(link)
        while True:
            status = await aria2_downloader.get_status(gid)
            if not status or status.get('status') == 'removed':
                await eor(message, f"Download {gid} cancelled or removed.")
                break

            if status.get('status') == 'active':
                progress = int(status['completedLength']) / int(status['totalLength']) * 100
                speed = float(status['downloadSpeed']) / 1024 / 1024
                file_name = status['files'][0]['path'].split('/')[-1]
                await eor(message, f"Downloading {file_name} ({progress:.2f}%) at {speed:.2f} MB/s")
            elif status.get('status') == 'complete':
                file_path = status['files'][0]['path']
                await eor(message, f"Download complete: {file_path}")
                return file_path
            elif status.get('status') == 'error':
                await eor(message, f"Download failed: {status['errorMessage']}")
                break
            await asyncio.sleep(5)
    elif link_type == 'youtube-dl':
        return await download_youtubedl(link, message)
    else:
        await eor(message, "Unsupported link type.")
    return None

async def download_youtubedl(link, message: Message):
    file_path = None
    loop = asyncio.get_event_loop()
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [lambda d: loop.call_soon_threadsafe(download_progress_hook, d, message)],
        }

        # Run yt-dlp in a separate thread to avoid blocking the event loop
        info_dict = await loop.run_in_executor(executor, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(link, download=True))
        file_path = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info_dict)
        return file_path, info_dict
    except Exception as e:
        await eor(message, f"yt-dlp download failed: {e}")
    return None, None

def download_progress_hook(d, message):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            percentage = (downloaded_bytes / total_bytes) * 100
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)

            asyncio.create_task(
                eor(message, f"📥 Downloading: {percentage:.2f}% | Speed: {format_bytes(speed)}/s | ETA: {format_seconds(eta)}")
            )
    elif d['status'] == 'finished':
        asyncio.create_task(
            eor(message, "✅ Download finished. Preparing to upload...")
        )

def format_bytes(bytes_val):
    if bytes_val is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0

def format_seconds(seconds):
    if seconds is None:
        return "N/A"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:d}h {m:02d}m {s:02d}s"

def format_duration_human_readable(seconds):
    if seconds is None:
        return "N/A"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_views_human_readable(views):
    if views is None:
        return "N/A"
    return f"{views:,}"