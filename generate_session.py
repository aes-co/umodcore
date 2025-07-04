# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env file
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    print("\n❌ Error: API_ID dan API_HASH tidak ditemukan di file .env")
    print("ℹ️ Pastikan kamu sudah mengisi API_ID dan API_HASH di file .env")
    exit(1)

print("\n🔐 Generating session string...")
print("ℹ️ Masukkan nomor telepon dan kode verifikasi saat diminta.")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    session_str = client.session.save()
    
    # Update .env file with session string
    with open(".env", "r") as f:
        lines = f.readlines()
    
    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("SESSION_STRING="):
                f.write(f'SESSION_STRING={session_str}\n')
            else:
                f.write(line)
    
    print("\n✅ SESSION_STRING berhasil digenerate!")
    print("🧵 SESSION_STRING sudah disuntik ke file .env!")
    print("\n⚠️ JANGAN BAGIKAN session string ini ke siapapun!")
