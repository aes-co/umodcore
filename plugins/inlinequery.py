from telethon import events
from utils.core import register_command, eor, handle_error

def register_inlinequery(client):
    @register_command(client, "inline")
    @handle_error
    async def inline_query(event):
        """
        Dummy inline query support.
        Usage: .inline <query>
        """
        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "Usage: .inline <query>")
            return

        query = args[1]
        # For demonstration, just echo the query
        await eor(event, f"Inline query received: {query}")
