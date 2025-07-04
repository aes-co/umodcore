from telethon import events, Button
from telethon.tl.types import InputMessagesFilterEmpty
from utils.core import register_command, eor, handle_error
from utils.db import get_db_collection
import json

def register_customcmd(client):
    @register_command(client, "addcmd")
    @handle_error
    async def add_command(event):
        """
        Add a custom command shortcut.
        Usage: .addcmd <command> <response>
        """
        args = event.text.split(maxsplit=2)
        if len(args) < 3:
            await eor(event, "Usage: .addcmd <command> <response>")
            return

        cmd = args[1].lower()
        response = args[2]

        db = get_db_collection("custom_commands")
        existing = await db.find_one({"command": cmd})
        if existing:
            await eor(event, f"Command `{cmd}` already exists.")
            return

        await db.insert_one({"command": cmd, "response": response})
        await eor(event, f"Custom command `{cmd}` added successfully.")

    @register_command(client, "delcmd")
    @handle_error
    async def delete_command(event):
        """
        Delete a custom command shortcut.
        Usage: .delcmd <command>
        """
        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "Usage: .delcmd <command>")
            return

        cmd = args[1].lower()
        db = get_db_collection("custom_commands")
        result = await db.delete_one({"command": cmd})
        if result.deleted_count == 0:
            await eor(event, f"Command `{cmd}` not found.")
        else:
            await eor(event, f"Custom command `{cmd}` deleted successfully.")

    @register_command(client, "listcmd")
    @handle_error
    async def list_commands(event):
        """
        List all custom command shortcuts.
        Usage: .listcmd
        """
        db = get_db_collection("custom_commands")
        cursor = db.find({})
        commands = await cursor.to_list(length=100)
        if not commands:
            await eor(event, "No custom commands found.")
            return

        msg = "Custom Commands:\n"
        for cmd in commands:
            msg += f"• `{cmd['command']}`: {cmd['response']}\n"

        await eor(event, msg)

    @client.on(events.NewMessage(pattern=r"^\.(\w+)", outgoing=True))
    async def handle_custom_command(event):
        cmd = event.pattern_match.group(1).lower()
        db = get_db_collection("custom_commands")
        doc = await db.find_one({"command": cmd})
        if doc:
            await event.respond(doc["response"])
            await event.delete()
