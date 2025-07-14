import os
import gzip
import json
import asyncio
import logging
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

MONGO_URI: Optional[str] = os.getenv("MONGO_URI", None)
DB_NAME: str = os.getenv("MONGO_DB_NAME", "umodcore")

class MongoDB:
    """MongoDB client wrapper for async operations"""

    def __init__(self) -> None:
        if not MONGO_URI:
            logger.warning("MongoDB URI not set. MongoDB features disabled.")
            self.client: Optional[AsyncIOMotorClient] = None
            self.db = None
        else:
            self.client = AsyncIOMotorClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            logger.info(f"Connected to MongoDB database: {DB_NAME}")

    async def get_sudo_users(self) -> List[int]:
        """Retrieve sudo users from MongoDB"""
        if not self.db:
            return []
        cursor = self.db.sudo_users.find({})
        users = []
        async for doc in cursor:
            users.append(doc["user_id"])
        return users

    async def add_sudo_user(self, user_id: int) -> None:
        """Add a sudo user to MongoDB"""
        if not self.db:
            return
        await self.db.sudo_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )

    async def remove_sudo_user(self, user_id: int) -> None:
        """Remove a sudo user from MongoDB"""
        if not self.db:
            return
        await self.db.sudo_users.delete_one({"user_id": user_id})

    async def backup_to_local(self, backup_path: str = "backup_sudo_users.json.gz") -> None:
        """Backup sudo users to a local gzip JSON file"""
        if not self.db:
            logger.warning("MongoDB not connected. Cannot backup.")
            return
        users = await self.get_sudo_users()
        data = {"sudo_users": users}
        try:
            with gzip.open(backup_path, "wt", encoding="utf-8") as f:
                json.dump(data, f)
            logger.info(f"Backup saved to {backup_path}")
        except Exception as e:
            logger.error(f"Failed to save backup: {e}")

    async def restore_from_local(self, backup_path: str = "backup_sudo_users.json.gz") -> None:
        """Restore sudo users from a local gzip JSON file"""
        if not self.db:
            logger.warning("MongoDB not connected. Cannot restore.")
            return
        try:
            with gzip.open(backup_path, "rt", encoding="utf-8") as f:
                data = json.load(f)
            users = data.get("sudo_users", [])
            # Clear current collection
            await self.db.sudo_users.delete_many({})
            # Insert restored users
            if users:
                docs = [{"user_id": uid} for uid in users]
                await self.db.sudo_users.insert_many(docs)
            logger.info(f"Restored sudo users from {backup_path}")
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")

    async def set_welcome_message(self, chat_id: int, message: str) -> None:
        """Set welcome message for a chat"""
        if not self.db:
            return
        await self.db.welcome.update_one(
            {"chat_id": chat_id},
            {"$set": {"message": message}},
            upsert=True
        )

    async def get_welcome_message(self, chat_id: int) -> Optional[str]:
        """Get welcome message for a chat"""
        if not self.db:
            return None
        doc = await self.db.welcome.find_one({"chat_id": chat_id})
        return doc["message"] if doc else None

    async def clear_welcome_message(self, chat_id: int) -> None:
        """Clear welcome message for a chat"""
        if not self.db:
            return
        await self.db.welcome.delete_one({"chat_id": chat_id})

    async def set_restart_info(self, chat_id: int, timestamp: float) -> None:
        """Set restart info in DB"""
        if not self.db:
            return
        await self.db.restart.update_one(
            {"_id": "restart_info"},
            {"$set": {"chat_id": chat_id, "timestamp": timestamp}},
            upsert=True
        )

    async def get_restart_info(self) -> Optional[dict]:
        """Get and delete restart info from DB"""
        if not self.db:
            return None
        return await self.db.restart.find_one_and_delete({"_id": "restart_info"})

    async def set_user_cookies(self, user_id: int, cookies_content: str) -> None:
        """Set user cookies in DB"""
        if not self.db:
            return
        await self.db.cookies.update_one(
            {"user_id": user_id},
            {"$set": {"cookies": cookies_content}},
            upsert=True
        )

    async def get_user_cookies(self, user_id: int) -> Optional[str]:
        """Get user cookies from DB"""
        if not self.db:
            return None
        doc = await self.db.cookies.find_one({"user_id": user_id})
        return doc["cookies"] if doc else None

    async def delete_user_cookies(self, user_id: int) -> None:
        """Delete user cookies from DB"""
        if not self.db:
            return
        await self.db.cookies.delete_one({"user_id": user_id})

# Helper for plugin DB collection (for compatibility with plugins)
def get_db_collection(name: str):
    if hasattr(mongodb, 'db') and mongodb.db:
        return mongodb.db[name]
    raise RuntimeError('MongoDB is not configured or not available.')

# Singleton instance
mongodb = MongoDB()
