from telethon import events
from utils.core import register_command, eor, handle_error
import json
import os

LANG_DIR = "lang"
DEFAULT_LANG = "en"

def load_language(lang_code):
    path = os.path.join(LANG_DIR, f"{lang_code}.json")
    if not os.path.exists(path):
        path = os.path.join(LANG_DIR, f"{DEFAULT_LANG}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

user_languages = {}

def register_multilang(client):
    @register_command(client, "setlang")
    @handle_error
    async def set_language(event):
        """
        Set user preferred language.
        Usage: .setlang <language_code>
        """
        args = event.text.split(maxsplit=1)
        if len(args) < 2:
            await eor(event, "Usage: .setlang <language_code>")
            return

        lang_code = args[1].lower()
        # Check if language file exists
        path = os.path.join(LANG_DIR, f"{lang_code}.json")
        if not os.path.exists(path):
            await eor(event, f"Language '{lang_code}' not supported.")
            return

        user_languages[event.sender_id] = lang_code
        await eor(event, f"Language set to {lang_code}.")

    @client.on(events.NewMessage)
    async def greet_user(event):
        lang_code = user_languages.get(event.sender_id, DEFAULT_LANG)
        lang_data = load_language(lang_code)
        greeting = lang_data.get("greeting", "Hello!")
        if event.is_private and event.raw_text.lower() == "hi":
            await event.reply(greeting)
