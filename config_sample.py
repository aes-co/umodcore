# Sample Configuration for uModCore Userbot
# Copy this file to config.py and fill in your values

# Telegram API credentials (get from https://my.telegram.org)
API_ID = 12345678  # Your API ID
API_HASH = "your_api_hash_here"  # Your API Hash
SESSION_STRING = "your_session_string_here"  # Generate using generate_session.py

# Bot owner configuration
OWNER_ID = 123456789  # Your Telegram user ID
OWNER_USERNAME = "your_username_here"  # Your username without @

# Optional configurations
LOG_CHANNEL = -123456789  # Log channel ID (optional, use negative for channels)
SOURCE_CODE = "https://github.com/aes-co/umodcore"  # Source code URL

# Performance settings for high-volume usage (30k+ groups)
# These are automatically optimized in the code
# RATE_LIMIT = 0.1  # Message rate limit in seconds (100ms)
# QUEUE_SIZE = 1000  # Maximum queue size per chat
# TIMEOUT = 10.0  # Command timeout in seconds

# Database settings (if using database features)
# DATABASE_URL = "sqlite:///userbot.db"  # SQLite database path

# MongoDB settings for data storage
MONGO_URI = "mongodb://localhost:27017"  # MongoDB connection URI
MONGO_DB_NAME = "umodcore"  # MongoDB database name

# Backup settings
BACKUP_PATH = "backup_sudo_users.json.gz"  # Local compressed backup file path

# Additional features
# AUTO_DELETE_TIMER = 30  # Auto-delete messages after N seconds
# MAX_CONCURRENT_COMMANDS = 50  # Maximum concurrent command processing
