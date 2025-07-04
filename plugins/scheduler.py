from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from datetime import datetime, timedelta
import re

scheduled_tasks = {}

def parse_time(time_str: str):
    """
    Parse time string like '10s', '5m', '2h', '1d' into seconds.
    """
    match = re.match(r"(\d+)([smhd])", time_str)
    if not match:
        return None
    value, unit = match.groups()
    value = int(value)
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    return None

def register_scheduler(app: Client):
    @app.on_message(filters.command("schedule", prefixes=".") & filters.me)
    async def schedule_message(client: Client, message: Message):
        """
        Schedule a message to be sent after a delay.
        Usage: .schedule <time> <message>
        Example: .schedule 10m Hello in 10 minutes!
        """
        if len(message.command) < 3:
            await message.reply("Usage: .schedule <time> <message>\nExample: .schedule 10m Hello in 10 minutes!")
            return

        time_str = message.command[1]
        delay = parse_time(time_str)
        if delay is None:
            await message.reply("Invalid time format! Use s, m, h, or d (e.g., 10m for 10 minutes).")
            return

        text = " ".join(message.command[2:])
        scheduled_time = datetime.now() + timedelta(seconds=delay)

        async def send_scheduled():
            await asyncio.sleep(delay)
            await message.reply(text)

        task = asyncio.create_task(send_scheduled())
        scheduled_tasks[message.message_id] = task

        await message.reply(f"Message scheduled to be sent in {time_str} at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

    @app.on_message(filters.command("cancelschedule", prefixes=".") & filters.me)
    async def cancel_schedule(client: Client, message: Message):
        """
        Cancel a scheduled message by message ID.
        Usage: .cancelschedule <message_id>
        """
        if len(message.command) < 2:
            await message.reply("Usage: .cancelschedule <message_id>")
            return

        try:
            msg_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid message ID.")
            return

        task = scheduled_tasks.get(msg_id)
        if task:
            task.cancel()
            del scheduled_tasks[msg_id]
            await message.reply(f"Cancelled scheduled message with ID {msg_id}.")
        else:
            await message.reply("No scheduled message found with that ID.")
