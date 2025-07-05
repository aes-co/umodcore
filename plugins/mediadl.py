import re
import os
import asyncio
from telethon import events
from utils.core import register_command, eor, handle_error
from utils.download_handler import handle_download, aria2_downloader, format_duration_human_readable, format_views_human_readable

def extract_clean_url(text):
    """Membersihkan link dari format Markdown dan mengekstrak URL yang valid."""
    match = re.search(r'\[?(https?://[^\s\]\)]+)', str(text))
    if match:
        return match.group(1)
    return None

def format_size(byte_size):
    """Mengubah ukuran byte menjadi format yang mudah dibaca (KB, MB, GB)."""
    if byte_size is None:
        return "N/A"
    power = 1024
    n = 0
    power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while byte_size > power and n < len(power_labels) - 1:
        byte_size /= power
        n += 1
    return f"{byte_size:.2f} {power_labels[n]}"

def generate_dynamic_caption(file_path, info_dict, url, sender_id):
    """Membuat caption secara dinamis berdasarkan tipe file (video, audio, atau file umum)."""
    # Nama bot telah diubah di sini
    footer = f'<b>⚡ Diunduh oleh:</b> <a href="tg://user?id={sender_id}"><b>Z4es Usebot</b></a>'
    
    # KASUS 1: Download dari yt-dlp (ada info_dict)
    if info_dict:
        title = info_dict.get('title', 'N/A')
        webpage_url = info_dict.get('webpage_url', url)
        
        # Cek jika ini adalah VIDEO
        if info_dict.get('vcodec') != 'none' and info_dict.get('height'):
            header = "<b>🎬 Informasi Video:</b>"
            duration = format_duration_human_readable(info_dict.get('duration'))
            views = format_views_human_readable(info_dict.get('view_count'))
            channel = info_dict.get('channel', 'N/A')
            resolution = f"{info_dict.get('width')}x{info_dict.get('height')}"
            
            return f"""<blockquote>{header}

<b>• Judul:</b> <code>{title}</code>
<b>• Resolusi:</b> <code>{resolution}</code>
<b>• Durasi:</b> <code>{duration}</code>
<b>• Dilihat:</b> <code>{views}</code>
<b>• Channel:</b> <code>{channel}</code>
<b>• Tautan:</b> <a href="{webpage_url}"><b>🔗 Klik Disini</b></a>

{footer}</blockquote>"""
        
        # Jika bukan video, anggap sebagai AUDIO
        else:
            header = "<b>🎵 Informasi Audio:</b>"
            duration = format_duration_human_readable(info_dict.get('duration'))
            views = format_views_human_readable(info_dict.get('view_count'))
            channel = info_dict.get('channel', 'N/A')

            return f"""<blockquote>{header}

<b>• Judul:</b> <code>{title}</code>
<b>• Durasi:</b> <code>{duration}</code>
<b>• Dilihat:</b> <code>{views}</code>
<b>• Channel:</b> <code>{channel}</code>
<b>• Tautan:</b> <a href="{webpage_url}"><b>🔗 Klik Disini</b></a>

{footer}</blockquote>"""

    # KASUS 2: Download biasa/langsung (tidak ada info_dict)
    else:
        header = "<b>🗂️ Informasi File:</b>"
        filename = os.path.basename(file_path)
        filesize = format_size(os.path.getsize(file_path))

        return f"""<blockquote>{header}

<b>• Nama File:</b> <code>{filename}</code>
<b>• Ukuran:</b> <code>{filesize}</code>
<b>• Tautan Asal:</b> <code>{url}</code>

{footer}</blockquote>"""


def register_mediadl(client):
    @register_command(client, "dl")
    @handle_error
    async def download_and_upload_media(event):
        full_command_text = event.text
        command_prefix = ".dl"
        
        if full_command_text.lower().startswith(command_prefix + " "):
            raw_url = full_command_text[len(command_prefix + " "):].strip()
        else:
            await eor(event, "💡 **Penggunaan:** `.dl <url_atau_balas_ke_link>`")
            return
            
        url = extract_clean_url(raw_url)
        if not url:
            await eor(event, "⚠️ **URL tidak valid.** Mohon berikan link yang benar.")
            return

        message = await eor(event, f"📥 **Memulai unduhan dari:**\n`{url}`")
        
        download_result = await handle_download(url, message)
        
        if not download_result:
            await eor(message, "❌ **Gagal mengunduh.** Link mungkin tidak valid atau konten tidak tersedia.")
            return
            
        file_path, info_dict = download_result
        
        if file_path and os.path.exists(file_path):
            async def upload_progress_hook(current, total):
                percentage = (current / total) * 100
                try:
                    await eor(message, f"📤 **Mengunggah:** {percentage:.2f}%")
                except Exception:
                    pass

            await message.edit(f"✅ **Selesai Mengunduh!**\n📤 Sekarang mengunggah `{os.path.basename(file_path)}`...")
            
            caption = generate_dynamic_caption(file_path, info_dict, url, event.sender_id)
            
            await client.send_file(
                event.chat_id,
                file_path,
                caption=caption,
                parse_mode='html',
                reply_to=event.id,
                progress_callback=upload_progress_hook
            )
            await message.delete()
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error removing file: {e}")

    @register_command(client, "dlstatus")
    @handle_error
    async def download_status(event):
        status = await aria2_downloader.get_status()
        if not status:
            await eor(event, "🔌 **Koneksi Gagal:** Aria2c sedang tidak berjalan.")
            return

        msg = "📊 **Status Unduhan**\n\n"
        msg += f"⚡ **Kecepatan Global:** {format_size(status['global']['downloadSpeed'])}/s\n"
        msg += f"▶️ **Aktif:** {len(status['active'])} | ⏸️ **Menunggu:** {len(status['waiting'])} | ⏹️ **Berhenti:** {len(status['stopped'])}\n\n"

        if not status['active']:
            msg += "Tidak ada unduhan yang aktif saat ini."
        else:
            for dl in status['active']:
                if 'totalLength' in dl and int(dl['totalLength']) > 0:
                    progress = int(dl['completedLength']) / int(dl['totalLength']) * 100
                    msg += f"• `{dl['files'][0]['path'].split('/')[-1]}` ({progress:.2f}%)\n"
                else:
                    msg += f"• `{dl.get('gid')}` (Menghitung...)\n"

        await eor(event, msg)

    @register_command(client, "dlcancel")
    @handle_error
    async def cancel_download(event):
        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "💡 **Penggunaan:** `.dlcancel <gid>`")
            return
        
        gid = args[1]
        try:
            await aria2_downloader.cancel_download(gid)
            await eor(event, f"🗑️ **Batal:** Unduhan `{gid}` berhasil dibatalkan.")
        except Exception as e:
            await eor(event, f"❌ **Gagal:** Tidak dapat membatalkan unduhan `{gid}`: {e}")