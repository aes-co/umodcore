from telethon import events
from utils.core import register_command, eor, handle_error
from utils.db import get_db_collection, mongodb
from collections import Counter
import asyncio

def register_chatstats(client):
    @register_command(client, "chatstats")
    @handle_error
    async def chat_statistics(event):
        """
        Show chat statistics: total messages, active users count, top active users.
        Usage: .chatstats
        """
        chat = await event.get_chat()
        if not chat:
            await eor(event, "Tidak dapat mengambil informasi chat.")
            return

        db = get_db_collection("chat_messages")
        # Aggregate message counts per user in this chat
        pipeline = [
            {"$match": {"chat_id": chat.id}},
            {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_users = await db.aggregate(pipeline).to_list(length=10)

        total_messages = await db.count_documents({"chat_id": chat.id})

        msg = f"📊 Statistik Chat untuk <b>{chat.title or chat.first_name}</b>:\n"
        msg += f"• Total Pesan: {total_messages}\n"
        msg += f"• Pengguna Aktif Teratas:\n"

        if not top_users:
            msg += "  Tidak ada data pengguna aktif."
        else:
            for i, user_stat in enumerate(top_users, 1):
                user_id = user_stat["_id"]
                count = user_stat["count"]
                try:
                    user = await client.get_entity(user_id)
                    name = user.first_name or "Unknown"
                except:
                    name = "Unknown"
                msg += f"  {i}. {name} - {count} pesan\n"

        await eor(event, msg)

    @client.on(events.NewMessage)
    async def track_messages(event):
        # Track messages for statistics
        if event.is_private or not mongodb.db:
            return  # Skip private chats and if no db

        db = get_db_collection("chat_messages")
        doc = {
            "chat_id": event.chat_id,
            "user_id": event.sender_id,
            "message_id": event.id,
            "date": event.date
        }
        await db.insert_one(doc)
