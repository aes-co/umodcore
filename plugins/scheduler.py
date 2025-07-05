from telethon import events
import asyncio
from datetime import datetime, timedelta
import re
from utils.core import register_command, eor, handle_error

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

def register_scheduler(client):
    @register_command(client, "schedule")
    @handle_error
    async def schedule_message(event):
        """
        Schedule a message to be sent after a delay.
        Usage: .schedule <time> <message>
        Example: .schedule 10m Hello in 10 minutes!
        """
        args = event.raw_text.split(maxsplit=2)
        if len(args) < 3:
            await eor(event, "Usage: .schedule <time> <message>\nExample: .schedule 10m Hello in 10 minutes!")
            return
        time_str = args[1]
        delay = parse_time(time_str)
        if delay is None:
            await eor(event, "Invalid time format! Gunakan s, m, h, atau d (cth: 10m untuk 10 menit).")
            return
        text = args[2]
        scheduled_time = datetime.now() + timedelta(seconds=delay)
        async def send_scheduled():
            await asyncio.sleep(delay)
            await event.reply(text)
        task = asyncio.create_task(send_scheduled())
        scheduled_tasks[event.id] = task
        await eor(event, f"Pesan dijadwalkan dalam {time_str} pada {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

    @register_command(client, "cancelschedule")
    @handle_error
    async def cancel_schedule(event):
        """
        Cancel a scheduled message by message ID.
        Usage: .cancelschedule <message_id>
        """
        args = event.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "Usage: .cancelschedule <message_id>")
            return
        try:
            msg_id = int(args[1])
        except ValueError:
            await eor(event, "Invalid message ID.")
            return
        task = scheduled_tasks.get(msg_id)
        if task:
            task.cancel()
            del scheduled_tasks[msg_id]
            await eor(event, f"Dibatalkan pesan terjadwal dengan ID {msg_id}.")
        else:
            await eor(event, "Tidak ditemukan pesan terjadwal dengan ID tersebut.")
