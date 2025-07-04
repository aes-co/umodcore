from telethon import events
from utils.core import register_command, eor, handle_error
from utils.db import get_db_collection

def register_reputation(client):
    @register_command(client, "rep")
    @handle_error
    async def show_reputation(event):
        """
        Show reputation of a user.
        Usage: .rep (reply to user)
        """
        if not event.is_reply:
            await eor(event, "Reply to a user's message to see their reputation.")
            return

        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id

        db = get_db_collection("user_reputation")
        doc = await db.find_one({"user_id": user_id})
        rep = doc["rep"] if doc else 0

        await eor(event, f"User reputation: {rep}")

    @register_command(client, "uprep")
    @handle_error
    async def upvote_reputation(event):
        """
        Upvote a user's reputation.
        Usage: .uprep (reply to user)
        """
        if not event.is_reply:
            await eor(event, "Reply to a user's message to upvote their reputation.")
            return

        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id

        db = get_db_collection("user_reputation")
        doc = await db.find_one({"user_id": user_id})
        rep = doc["rep"] if doc else 0
        rep += 1
        await db.update_one({"user_id": user_id}, {"$set": {"rep": rep}}, upsert=True)

        await eor(event, f"User reputation increased to {rep}")

    @register_command(client, "downrep")
    @handle_error
    async def downvote_reputation(event):
        """
        Downvote a user's reputation.
        Usage: .downrep (reply to user)
        """
        if not event.is_reply:
            await eor(event, "Reply to a user's message to downvote their reputation.")
            return

        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id

        db = get_db_collection("user_reputation")
        doc = await db.find_one({"user_id": user_id})
        rep = doc["rep"] if doc else 0
        rep -= 1
        await db.update_one({"user_id": user_id}, {"$set": {"rep": rep}}, upsert=True)

        await eor(event, f"User reputation decreased to {rep}")
