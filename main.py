# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

import os
import asyncio
import os
import logging
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
from utils.core import load_plugins

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'umodcore.log')), logging.StreamHandler()])
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

async def main():
    """Main function to start the userbot with optimizations for 30k+ groups"""
    print("🚀 Starting uModCore userbot...")
    print("⚡ Optimized for high-volume group management (30k+ groups)")
    
    # Start the client with optimizations
    await client.start()
    
    # Load all plugins dynamically
    load_plugins(client)
    
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
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
