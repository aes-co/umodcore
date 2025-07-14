# ModCore - UserBot (Telethon Version)
# Copyright (C) 2025 aeswnh

from telethon import TelegramClient, events
from telethon.tl.types import User, Message
from functools import wraps
from typing import Callable, Union, List, Optional, Tuple
import logging
import json
import contextvars
import datetime
import time
import asyncio
import os
from dotenv import load_dotenv
from collections import defaultdict
from utils.db import mongodb

# Load environment variables
load_dotenv()

# Get configuration from environment
OWNER_ID: int = int(os.getenv("OWNER_ID"))
OWNER_USERNAME: Optional[str] = os.getenv("OWNER_USERNAME")
LOG_CHANNEL: Optional[int] = int(os.getenv("LOG_CHANNEL")) if os.getenv("LOG_CHANNEL") else None
SOURCE_CODE: str = os.getenv("SOURCE_CODE", "https://github.com/aes-co/umodcore")

# Sudo users management with MongoDB fallback
SUDO_USERS: set[int] = set()

async def load_sudo_users() -> None:
    """Load sudo users from MongoDB or fallback to local file"""
    global SUDO_USERS
    if mongodb.db:
        try:
            users = await mongodb.get_sudo_users()
            SUDO_USERS = set(users)
            return
        except Exception as e:
            logging.error(f"Error loading sudo users from MongoDB: {e}")
    # Fallback to local file
    try:
        if os.path.exists("sudo_users.txt"):
            with open("sudo_users.txt", 'r') as f:
                SUDO_USERS = set(int(line.strip()) for line in f if line.strip().isdigit())
    except Exception as e:
        logging.error(f"Error loading sudo users from file: {e}")

async def save_sudo_users() -> None:
    """Save sudo users to MongoDB and local file"""
    if mongodb.db:
        try:
            # Clear collection and insert current users
            await mongodb.db.sudo_users.delete_many({})
            if SUDO_USERS:
                docs = [{"user_id": uid} for uid in SUDO_USERS]
                await mongodb.db.sudo_users.insert_many(docs)
        except Exception as e:
            logging.error(f"Error saving sudo users to MongoDB: {e}")
    # Save to local file as backup
    try:
        with open("sudo_users.txt", 'w') as f:
            for user_id in SUDO_USERS:
                f.write(f"{user_id}\n")
    except Exception as e:
        logging.error(f"Error saving sudo users to file: {e}")

async def add_sudo_user(user_id: int) -> None:
    """Add user to sudo list"""
    SUDO_USERS.add(user_id)
    await save_sudo_users()

async def remove_sudo_user(user_id: int) -> None:
    """Remove user from sudo list"""
    SUDO_USERS.discard(user_id)
    await save_sudo_users()

def is_sudo_user(user_id: int) -> bool:
    """Check if user is sudo"""
    return user_id in SUDO_USERS

def is_admin(user_id: int) -> bool:
    """Check if user is owner or sudo"""
    return user_id == OWNER_ID or is_sudo_user(user_id)

# Load sudo users on startup asynchronously
asyncio.get_event_loop().run_until_complete(load_sudo_users())

# High-performance message queue system for 30k+ groups
message_queues: defaultdict[int, asyncio.Queue] = defaultdict(asyncio.Queue)
last_message_time: defaultdict[int, float] = defaultdict(float)
queue_processors: dict[int, asyncio.Task] = {}
RATE_LIMIT: float = 0.1  # Reduced to 100ms for faster processing

async def process_message_queue(chat_id: int) -> None:
    """Process messages in queue for a specific chat with optimized rate limiting"""
    while True:
        try:
            func, args, kwargs = await message_queues[chat_id].get()
            current_time = time.time()
            
            # Optimized rate limiting for high volume
            time_since_last = current_time - last_message_time[chat_id]
            if time_since_last < RATE_LIMIT:
                await asyncio.sleep(RATE_LIMIT - time_since_last)
            
            # Execute the function with timeout
            try:
                await asyncio.wait_for(func(*args, **kwargs), timeout=10.0)
            except asyncio.TimeoutError:
                logging.error(f"Message timeout for chat {chat_id}")
                
            last_message_time[chat_id] = time.time()
            message_queues[chat_id].task_done()
            
        except Exception as e:
            logging.error(f"Error processing message queue for chat {chat_id}: {e}")
            continue

async def queue_message(chat_id: int, func: Callable, *args, **kwargs) -> None:
    """Add message to queue with optimized processor management"""
    # Start processor if not already running
    if chat_id not in queue_processors:
        queue_processors[chat_id] = asyncio.create_task(
            process_message_queue(chat_id)
        )
    
    # Add message to queue (non-blocking)
    try:
        message_queues[chat_id].put_nowait((func, args, kwargs))
    except asyncio.QueueFull:
        # If queue is full, process immediately without queue
        try:
            await func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error processing message immediately: {e}")

async def send_message_queued(client: TelegramClient, chat_id: int, *args, **kwargs) -> None:
    """Queue message send with rate limiting"""
    await queue_message(chat_id, client.send_message, chat_id, *args, **kwargs)

async def edit_message_queued(message: Message, *args, **kwargs) -> None:
    """Queue message edit with rate limiting"""
    await queue_message(message.chat_id, message.edit, *args, **kwargs)

async def reply_message_queued(message: Message, *args, **kwargs) -> None:
    """Queue message reply with rate limiting"""
    await queue_message(message.chat_id, message.reply, *args, **kwargs)

# Setup logging
logger = logging.getLogger(__name__)

# Context variable for structured logging context
log_context: contextvars.ContextVar[dict] = contextvars.ContextVar("log_context", default={})

class ContextFilter(logging.Filter):
    """Inject contextual information into log records"""
    def filter(self, record):
        context = log_context.get({})
        for key, value in context.items():
            setattr(record, key, value)
        return True

# Add context filter to logger
logger.addFilter(ContextFilter())

def set_log_context(**kwargs):
    """Set context variables for logging"""
    current_context = log_context.get().copy()
    current_context.update(kwargs)
    log_context.set(current_context)

def clear_log_context():
    """Clear logging context"""
    log_context.set({})

# Helper function for structured logging
def log_info(message: str, **kwargs):
    set_log_context(**kwargs)
    logger.info(message)
    clear_log_context()


def log_error(message: str, **kwargs):
    set_log_context(**kwargs)
    logger.error(message)
    clear_log_context()


# Global state management
class BotState:
    """Class to manage global bot state such as AFK users and command stats"""
    def __init__(self) -> None:
        self.start_time: float = time.time()
        self.command_count: int = 0
        self.last_command_time: Optional[float] = None
        self.active_commands: set[int] = set()
        self.afk_users: dict[int, dict[str, Union[str, 'datetime.datetime']]] = {}  # user_id: {since: datetime, reason: str, name: str}

    def set_afk(self, user_id: int, name: str, reason: Optional[str] = None) -> None:
        """Set a user as AFK"""
        from datetime import datetime
        self.afk_users[user_id] = {
            "since": datetime.now(),
            "reason": reason or "AFK tanpa alasan.",
            "name": name
        }

    def remove_afk(self, user_id: int) -> Optional[dict]:
        """Remove AFK status of a user"""
        return self.afk_users.pop(user_id, None)

    def get_afk_status(self, user_id: int) -> Optional[dict]:
        """Get AFK status of a user"""
        return self.afk_users.get(user_id)

    def is_afk(self, user_id: int) -> bool:
        """Check if a user is AFK"""
        return user_id in self.afk_users

bot_state = BotState()

# Permission decorators
def owner_only(func: Callable) -> Callable:
    """Decorator to allow only owner to use command"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        if event.sender_id == OWNER_ID:
            return await func(event, *args, **kwargs)
        else:
            await reply_message_queued(event, "⛔ Perintah ini hanya untuk owner bot!")
    return wrapper

def admin_only(func: Callable) -> Callable:
    """Decorator to allow only owner and sudo users to use command"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        if is_admin(event.sender_id):
            return await func(event, *args, **kwargs)
        else:
            await reply_message_queued(event, "⛔ Perintah ini hanya untuk admin bot!")
    return wrapper

def log_command(func: Callable) -> Callable:
    """Decorator to log command usage"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        bot_state.command_count += 1
        bot_state.last_command_time = time.time()
        command = event.raw_text.split()[0] if event.raw_text else "Unknown"
        logger.info(f"Command used: {command} by {event.sender_id}")
        return await func(event, *args, **kwargs)
    return wrapper

async def eor(event, text: str, **kwargs) -> Optional[Message]:
    """Edit or reply to a message with queue management"""
    try:
        if event.out:
            # For outgoing messages, edit directly without queue for better performance
            return await event.edit(text, **kwargs)
        else:
            # For incoming messages, reply with queue management
            return await event.reply(text, **kwargs)
    except Exception as e:
        logger.error(f"Error in eor function: {e}")
        # Fallback to direct reply if queue fails
        try:
            return await event.reply(text, **kwargs)
        except Exception as fallback_error:
            logger.error(f"Fallback reply also failed: {fallback_error}")
            return None

def log_command(func: Callable) -> Callable:
    """Decorator to log command usage"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        bot_state.command_count += 1
        bot_state.last_command_time = time.time()
        command = event.raw_text.split()[0] if event.raw_text else "Unknown"
        logger.info(f"Command used: {command} by {event.sender_id}")
        return await func(event, *args, **kwargs)
    return wrapper

async def eor(event, text: str, **kwargs) -> Optional[Message]:
    """Edit or reply to a message with queue management"""
    try:
        if event.out:
            # For outgoing messages, edit directly without queue for better performance
            return await event.edit(text, **kwargs)
        else:
            # For incoming messages, reply with queue management
            return await event.reply(text, **kwargs)
    except Exception as e:
        logger.error(f"Error in eor function: {e}")
        # Fallback to direct reply if queue fails
        try:
            return await event.reply(text, **kwargs)
        except Exception as fallback_error:
            logger.error(f"Fallback reply also failed: {fallback_error}")
            return None
async def delete_after(event, seconds: int = 5) -> None:
     """Delete a message after specified seconds"""
     try:
         await asyncio.sleep(seconds)
         await event.delete()
     except Exception as e:
         logger.error(f"Error deleting message: {e}")

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
        
    return " ".join(parts)

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
        
    return " ".join(parts)

def log_command(func: Callable) -> Callable:
    """Decorator to log command usage"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        bot_state.command_count += 1
        bot_state.last_command_time = time.time()
        command = event.raw_text.split()[0] if event.raw_text else "Unknown"
        logger.info(f"Command used: {command} by {event.sender_id}")
        return await func(event, *args, **kwargs)
    return wrapper

# Optimized message handling utilities
async def eor(event, text: str, **kwargs) -> Optional[Message]:
    """Edit or reply to a message with queue management"""
    try:
        if event.out:
            # For outgoing messages, edit directly without queue for better performance
            return await event.edit(text, **kwargs)
        else:
            # For incoming messages, reply with queue management
            return await event.reply(text, **kwargs)
    except Exception as e:
        logger.error(f"Error in eor function: {e}")
        # Fallback to direct reply if queue fails
        try:
            return await event.reply(text, **kwargs)
        except Exception as fallback_error:
            logger.error(f"Fallback reply also failed: {fallback_error}")
            return None

async def delete_after(event, seconds: int = 5) -> None:
    """Delete a message after specified seconds"""
    try:
        await asyncio.sleep(seconds)
        await event.delete()
    except Exception as e:
        logger.error(f"Error deleting message: {e}")

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable string"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
        
    return " ".join(parts)

# Command registration helper with concurrent processing
def register_command(
    client: TelegramClient,
    pattern: str,
    owner_only: bool = False,
    **kwargs
) -> Callable:
    """Helper to register commands with common filters and concurrent processing"""
    def decorator(func: Callable) -> Callable:
        pattern_str = f"^\\.{pattern}(?:\\s|$)"
        
        @events.register(events.NewMessage(pattern=pattern_str, **kwargs))
        @wraps(func)
        async def command_handler(event):
            # Process commands concurrently for better performance
            asyncio.create_task(handle_command(event, func, owner_only))
                
        client.add_event_handler(command_handler)
        return command_handler
    return decorator

async def handle_command(event, func: Callable, owner_only_check: bool) -> None:
    """Handle command execution with error handling"""
    try:
        if owner_only_check and event.sender_id != OWNER_ID:
            await reply_message_queued(event, "⛔ Perintah ini hanya untuk owner bot!")
            return
        await func(event)
    except Exception as e:
        logger.error(f"Error in command: {e}")
        await eor(event, f"❌ Terjadi kesalahan tak terduga. Insiden ini telah dicatat.")

# Error handling
def handle_error(func: Callable) -> Callable:
    """Decorator for consistent error handling"""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            await eor(event, "❌ Terjadi kesalahan tak terduga. Insiden ini telah dicatat.")
    return wrapper

# Message formatting helpers
def code_block(text: str) -> str:
    """Wrap text in code block"""
    return f"```\n{text}\n```"

def bold(text: str) -> str:
    """Make text bold"""
    return f"**{text}**"

def italic(text: str) -> str:
    """Make text italic"""  
    return f"_{text}_"

# Plugin registration helper
def load_plugins(client: TelegramClient) -> None:
    """Dynamically load all plugins"""
    import os
    import importlib
    import sys
    # Ensure root project is in sys.path
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    plugins_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plugins')
    for file in os.listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("__"):
            plugin_name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{plugin_name}")
                register_function_name = f"register_{plugin_name}"
                if hasattr(module, register_function_name):
                    getattr(module, register_function_name)(client)
                    logger.info(f"Successfully loaded plugin: {plugin_name}")
                else:
                    logger.warning(f"Plugin {plugin_name} does not have a {register_function_name} function.")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_name}: {e}")

def reload_plugins(client: TelegramClient) -> Tuple[List[str], List[str]]:
    """Reload all plugins in the plugins directory"""
    import os
    import sys
    import importlib
    
    folder = "plugins"
    successful: List[str] = []
    failed: List[str] = []

    for file in os.listdir(folder):
        if file.endswith(".py") and not file.startswith("__"):
            plugin_name = file[:-3]
            modname = f"{folder}.{plugin_name}"
            try:
                if modname in sys.modules:
                    importlib.reload(sys.modules[modname])
                else:
                    importlib.import_module(modname)
                    
                module = sys.modules[modname]
                if hasattr(module, "register"):
                    module.register(client)
                    
                successful.append(plugin_name)
                logger.info(f"Successfully reloaded plugin: {plugin_name}")
            except Exception as e:
                failed.append(f"{plugin_name} → {str(e)}")
                logger.error(f"Failed to reload plugin {plugin_name}: {e}")

    return successful, failed

async def restart_bot(event) -> None:
    """Restart the userbot with notification"""
    import os
    import sys
    import time
    import asyncio
    
    # Save restart info
    with open(".restart_chat_id", "w") as f:
        f.write(str(event.chat_id))
    
    with open(".restart_time", "w") as t:
        t.write(str(time.time()))
    
    # Wait briefly then restart
    await asyncio.sleep(1)
    os.execv(sys.executable, [sys.executable, "main.py"])

def get_log_file() -> Optional[str]:
    """Get the path to the active log file"""
    import os
    
    # Check common log file names
    log_files = ["error.log", "log.txt"]
    for path in log_files:
        if os.path.exists(path):
            return path
    return None

# Bot info constants
REPO_MSG: str = """
🐾 **MODCORE USERBOT** 🐾

📦 Repo: [ModCore Userbot](https://github.com/aes-co/umodcore)
🧩 ModCore Bot: [Klik di sini](https://github.com/aes-co/modcore)
👑 Owner: @aeswnh
"""

from telethon.tl.types import KeyboardButtonUrl

REPO_BUTTONS = [
    [
        KeyboardButtonUrl("📦 Repo", "https://github.com/aes-co/umodcore"),
        KeyboardButtonUrl("🤖 ModCore Bot", "https://github.com/aes-co/modcore")
    ],
    [
        KeyboardButtonUrl("👤 Owner", f"https://t.me/{OWNER_USERNAME}")
    ]
]

INTRO_MSG: str = """✨ **Terima kasih telah menggunakan ModCore Userbot!**

🔧 Gunakan perintah `.help` untuk melihat daftar command.
📌 Jangan lupa cek repo dan dokumentasi ya!

**📋 Command Tersedia:**
• `.ping` - Test latency
• `.me` - Info akun kamu
• `.uinfo` - Info user lain
• `.afk [alasan]` - Set AFK mode
• `.speedtest` - Test kecepatan internet
• `.start` - Welcome message
• `.help` - Bantuan command

**⚙️ Admin Commands:**
• `.log [pesan]` - Kirim ke log channel
• `.restart` - Restart userbot
• `.reload` - Reload plugins
• `.auth @user` - Tambah sudo user
"""

PHOTO_URL: str = "https://octodex.github.com/images/mona-whisper.gif"

# State management helpers
def get_uptime() -> str:
    """Get bot uptime as formatted string"""
    return format_duration(time.time() - bot_state.start_time)

def get_command_count() -> int:
    """Get total number of commands executed"""
    return bot_state.command_count

def get_last_command_time() -> Optional[float]:
    """Get timestamp of last command execution"""
    return bot_state.last_command_time
