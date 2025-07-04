import os
import gzip
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from utils.core import logger

MONGO_URI = os.getenv("MONGO_URI", None)
DB_NAME = os.getenv("MONGO_DB_NAME", "umodcore")

class MongoDB:
    def __init__(self):
        if not MONGO_URI:
            logger.warning("MongoDB URI not set. MongoDB features disabled.")
            self.client = None
            self.db = None
        else:
            self.client = AsyncIOMotorClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            logger.info(f"Connected to MongoDB database: {DB_NAME}")

    async def get_sudo_users(self):
        if not self.db:
            return []
        cursor = self.db.sudo_users.find({})
        users = []
        async for doc in cursor:
            users.append(doc["user_id"])
        return users

    async def add_sudo_user(self, user_id: int):
        if not self.db:
            return
        await self.db.sudo_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )

    async def remove_sudo_user(self, user_id: int):
        if not self.db:
            return
        await self.db.sudo_users.delete_one({"user_id": user_id})

    async def backup_to_local(self, backup_path="backup_sudo_users.json.gz"):
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

    async def restore_from_local(self, backup_path="backup_sudo_users.json.gz"):
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

# Singleton instance
mongodb = MongoDB()
