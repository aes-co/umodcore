# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

from pyrogram import Client
import asyncio

import config

async def main():
    async with Client(
        name="generate_session",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        in_memory=True
    ) as app:
        session_str = await app.export_session_string()
        print("\n✅ SESSION_STRING berhasil digenerate!")

        with open("config.py", "r") as f:
            lines = f.readlines()

        with open("config.py", "w") as f:
            for line in lines:
                if line.startswith("SESSION_STRING"):
                    f.write(f'SESSION_STRING = "{session_str}"\n')
                else:
                    f.write(line)

        print("🧵 SESSION_STRING sudah disuntik ke config.py!")

if __name__ == "__main__":
    asyncio.run(main())
